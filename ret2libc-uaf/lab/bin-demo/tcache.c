#include <stdio.h>
#include <stdlib.h>

__attribute__((constructor))
void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
        setbuf(stderr, NULL);
}

int main(void)
{
        void *storage[7];

        for (size_t sz = 0x20; sz <= 0x410; sz += 0x10) {
                // Allocate 7 distinct chunks for the current size
                for (int i = 0; i < 7; i++) {
                        storage[i] = malloc(sz - 0x10);
                }
                // Free all 7 to fill the tcache bin for this size
                for (int i = 0; i < 7; i++) {
                        free(storage[i]);
                }
        }

        getchar();
        return 0;
}
