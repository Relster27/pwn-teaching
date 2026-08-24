#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

char shellcode[] =
"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68"
"\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05";

int main(void)
{
        printf("[*] Allocating RWX memory...\n");
        void *execute_me = mmap(
            (void *)0xdead000,
            0x1000,
            PROT_READ | PROT_WRITE | PROT_EXEC, // Set memory to RWX
            MAP_PRIVATE | MAP_ANONYMOUS,        // flags
            -1,
            0
        );

        printf("[*] Copying shellcode...\n");
        memcpy(execute_me, shellcode, sizeof(shellcode));

        printf("[*] Jumping to shellcode at %p\n", execute_me);

        ((void(*)())execute_me)();      // execute shellcode
        return 0;
}

