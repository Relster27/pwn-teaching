#!/usr/bin/env python3

from pwn import *

TARGET = './chall'
HOST = ''
PORT = 1337

elf = ELF(TARGET)
libc = ELF('./libc.so.6', checksec=False)
ld = ELF('./ld-linux-x86-64.so.2', checksec=False)

context.arch = 'amd64'

gdb_script = f"""
  b *main
  c
"""
# context.log_level = 'DEBUG'

if args.GDB:
  # context.terminal = ['tmux', 'splitw', '-h']  
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

'''

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

def opt(idx: int, pay):
  p.sendlineafter(b'', str(idx).encode())

fs = FileStructure()

# ===================================== #

# pause()

p.interactive()

# NOTE:
#

