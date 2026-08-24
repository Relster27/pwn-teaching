#include <stdio.h>
#include <stdlib.h>
#include <string.h>

__attribute__((constructor))
void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
        setbuf(stdin, NULL);
}

int main(void)
{
        int smallest_sz_fastbin = 0x10;
        int biggest_sz_fastbin = 0x70; // 0x80

        char *chunks[8];

        for (int i = 0; i < sizeof(chunks)/8; i++) {
                chunks[i] = malloc(biggest_sz_fastbin); // ganti ke 0x10 untuk melihat perbedaan index di main_arena->fastbinsY
        }

        getchar();      // BREAKPOINT

        for (int i = 0; i < sizeof(chunks)/8; i++) {
                free(chunks[i]);
        }

        getchar();
        return 0;
}
