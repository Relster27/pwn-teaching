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
        int smallest_sz_largebin = 0x3f0; // 0x400
        int biggest_sz_largebin = 0xbfff0;

        char *chunks[8];

        for (int i = 0; i < sizeof(chunks)/8; i++) {
                chunks[i] = malloc(smallest_sz_largebin);      // ganti ke 0x3f0 untuk melihat perbedaan index di main_arena->bins
        }

        char *guard = malloc(0x20);

        for (int i = 0; i < sizeof(chunks)/8; i++) {
                free(chunks[i]);
        }

        getchar();
        char *x = malloc(0x500);        // alokasi dengan size yang besar biar malloc_consolidate dieksekusi
        free(x);
        // BREAK disini untuk melihat largebins

        getchar();
        free(chunks[0]);
        return 0;
}
