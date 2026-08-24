#!/usr/bin/env python3

from pwn import *

TARGET = './warmup'

elf = ELF(TARGET)

p = process(TARGET)

context.arch = 'amd64'
# context.arch = 'i386'
# context.log_level = 'debug'

# EXPLOIT DIBAWAH #

# p64()

p.interactive()
