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
        int amount = 8;
        char *h[amount];

        for (int i = 0; i < amount; i++) {
                h[i] = malloc(0x70);    // 0x80
        }

        // fastbins 0x20 - 0x80
        
        char *guard = malloc(0x10);

        for (int i = 0; i < amount; i++) {
                free(h[i]);
        }

        char *x = malloc(0x410); free(x);       // trigger malloc_consolidate
        // BREAK disini untuk melihat smallbins
        getchar();

        for (int i = 0; i < amount-1; i++) {
                h[i] = malloc(0x70);
        }
        getchar();
        char *y = malloc(0x10); // ambil chunk dari smallbins -> smallbins menjadi unsortedbin -> last remainder set
        // BREAK disini untuk melihat last_remainder

        getchar();
        return 0;
}
