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
        int smallest_sz_smallbin = 0x10;
        int biggest_sz_smallbin = 0x3e0;

        char *chunks[8];

        for (int i = 0; i < sizeof(chunks)/8; i++) {
                chunks[i] = malloc(biggest_sz_smallbin);        // ganti ke 0x10 untuk melihat perbedaan index di main_arena->bins
        }

        char *guard = malloc(0x20);

        for (int i = 0; i < sizeof(chunks)/8; i++) {
                free(chunks[i]);
        }

        char *x = malloc(0x420);        // alokasi dengan size yang besar biar malloc_consolidate dieksekusi
        free(x);
        // BREAK disini untuk melihat smallbins

        getchar();
        return 0;
}
