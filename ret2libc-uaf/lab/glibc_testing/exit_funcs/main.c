#include <stdio.h>
#include <stdlib.h>
#include <string.h>

__attribute__((constructor))
void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
        setbuf(stderr, NULL);
}

int main(void)
{
        long long *heap = malloc(0x30);
        heap[0] = 0x0;
        heap[1] = 0x1;
        heap[2] = 0x4;
        heap[3] = 0xdeadbeef;  // encrypted(system, pointer_guard)
        heap[4] = 0xcafebabe;  // pointer to string /bin/sh

        getchar();      // ganti kedua value diatas
        return 0;
}

