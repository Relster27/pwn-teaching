#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor))
void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
        __asm__("pop %rdi; ret;");
}

void leaky(unsigned long password)
{
        void *leak = system;
        if (password == 0xa59a12d) {
                write(1, &leak, 8);
        } else {
                write(1, "Belum bocor enough!\n", 20);
        }
}

void vuln(void)
{
        char vuln_buf[32];

        printf("?> ");
        read(0, vuln_buf, 80);        
}

int main(void)
{
        vuln();
        return 0;
}
