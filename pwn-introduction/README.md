TODO:
CHECK PROTECTIONS!!
- polish oob-read/          (flag global variable buffer??)
- recheck oob-write/
- polish oob-read-write/    (recompile with FULL RELRO, Canary, PIE)

Materials:
- ASCII
- Endianness
- Linux ELF memory layout
- Stack frame (rbp, rsp, saved return address)
- Assembly
- x86/64 Registers
- Binary protections (PIE, NX, RELRO, Canary)
- pwntools
- gdb (pwndbg, gef)
- basic rev using ghidra
[OPTIONAL??]
- pwninit
- how to read manpage

Techniques:
- Ret2win
[OPTIONAL??]
- ROP (Return Oriented Programming)
- Ret2plt / GOT overwrite
- Ret2libc
- Tcache poisoning
- Fastbin double-free
- FSOP
- SROP

Vulns:
- Integer overflow/underflow
- Stack buffer overflow
- Intentional/unintentional info leak
- Out-of-bound (OOB) read/write
[OPTIONAL??]
- Format string
- Shellcode
- Heap overflow
- Use-After-Free (UAF)
- Double-free

Extras:
- Browser exploitation
- Kernel exploitation
- Sandbox/Emu/VM escape

Link ppt: https://www.canva.com/design/DAG2_wywvlQ/Lw4L4KBD0Ua93ugwGvA0LQ/edit
