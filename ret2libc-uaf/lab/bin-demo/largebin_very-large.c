#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>

/* * mallopt constants to prevent mmap usage.
 * M_MMAP_THRESHOLD: maximum size before using mmap (we set it huge)
 * M_TRIM_THRESHOLD: prevent sbrk from releasing memory back to OS immediately
 */

__attribute__((constructor))
void init(void)
{
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stdin, NULL);

	// 1. Disable mmap for large allocations so they stay on the heap
        mallopt(M_MMAP_THRESHOLD, -1); 
        mallopt(M_TRIM_THRESHOLD, -1);
}

int main(void)
{
	size_t big_size = 1024 * 1024;
        void* big_chunk = malloc(big_size);

        char *guard = malloc(16); 

        free(big_chunk);

	getchar();
        void* trigger = malloc(big_size + 16);	// alokasi dengan size yang besar biar malloc_consolidate dieksekusi

        getchar();
    return 0;
}
