#include <stdio.h>

char global_buf[16] = {0};

void win(void)
{
        printf("win!!\n");
}

int main(void)
{
        puts(&scanf);
        printf("Input your index: ");
        int idx = 0;
        scanf("%d", &idx); getchar();

        printf("%llx\n", *(unsigned long long *)&global_buf[idx]);
        
        char buf[32];
        gets(buf);
        return 0;
}