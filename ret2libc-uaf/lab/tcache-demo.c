#include <stdio.h>
#include <stdlib.h>

// gcc file.c -o file -g -no-pie

int main(void)
{       
        // 0x20 - 0x410
        char *tcache = malloc(0x30); // 0x40
        scanf("%s", tcache);

        /*
        0x1234  0x0000000000000000 0x0000000000000041
        0x5678  0x0000000000000000 0x0000000000000000
        0x9abc  0x0000000000000000 0x0000000000000000
        0xdef0  0x0000000000000000 0x0000000000000000
        0xdead  0x0000000000000000 0x0000000000020d31
        */

        free(tcache);

        return 0;
}
