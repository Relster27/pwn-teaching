#!/usr/bin/env python3

from pwn import *

TARGET = './ret2win_32'

context.arch = 'i386'

elf = ELF(TARGET)
p = process(TARGET)

pause()
win1 = elf.symbols['win']        # <---- ini
win2 = elf.sym.win       # <---- ini
print(f"win1: {hex(win1)}")
print(f"win2: {hex(win2)}")
# payload = b'A' * 40 + b'B' * 4 + p32(win)
# p.sendlineafter(b'Input: ', payload)

p.interactive()
