#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor))
void init(void)
{
        setvbuf(stdout, NULL, _IONBF, 0);
        setvbuf(stderr, NULL, _IONBF, 0);
}

void banner(void)
{
        puts("Let's start easy!");
        puts("You should know what to do, right");
        printf(">> ");
}

int main(void)
{
        banner();
        long cookie = 0xffffeeeeffffeeee;
        char buf[32] = {0};
        
        read(0, buf, 48);

        if (cookie == 0x6769676967696769) {
                printf("FLAG: ");
                system("cat flag.txt");
        } else {
                printf("cookie: 0x%llx\n", cookie);
        }
        
        return 0;
}