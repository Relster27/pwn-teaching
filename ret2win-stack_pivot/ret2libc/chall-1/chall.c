#include <stdio.h>
#include <stdlib.h>

__attribute__((constructor))
void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
}

int main(void)
{
        char vuln_buffer[64];

        printf("Leak: %p\n", &scanf);

        printf("Langsung saja-> ");
        gets(vuln_buffer);

        return 0;
}
