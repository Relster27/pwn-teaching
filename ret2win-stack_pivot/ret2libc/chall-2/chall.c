#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define MAGIC (0xb00b00baabaa)
#define NO_MAGIC (0xad00d00)

__attribute__((constructor))
void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
}

void play(void)
{
        unsigned long hmm = MAGIC;
        char vuln_buf[32];

        printf(">>> ");
        read(0, vuln_buf, 48);

        if (hmm != MAGIC && (hmm == NO_MAGIC)) {
                printf("No more magic: %p\n", &exit);

                printf("==>> ");
                read(0, vuln_buf, sizeof(vuln_buf) * 3);
        } else {
                puts("I wonder what can you do without leak");
                printf("==>> ");
                read(0, vuln_buf, sizeof(vuln_buf) * 3);
        }
}

int main(void)
{
        play();
        return 0;
}
