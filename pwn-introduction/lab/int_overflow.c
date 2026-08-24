#include <stdio.h>
#include <limits.h>

int main(void)
{
        int max = INT_MAX;
        int min = INT_MIN;

        int overflow = max + 1;

        puts("");
        puts("");
        puts("");
        puts("");
        printf("max     : %d\n", max);
        printf("min     : %d\n", min);
        printf("overflow: %d\n", overflow);
        puts("");
        puts("");
        puts("");
        puts("");
        return 0;
}
