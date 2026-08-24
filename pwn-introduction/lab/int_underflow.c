#include <stdio.h>
#include <limits.h>

int main(void)
{
        int max = INT_MAX;
        int min = INT_MIN;

        int underflow = min - 1;

        printf("max      : %d\n", max);
        printf("min      : %d\n", min);
        printf("underflow: %d\n", underflow);
        return 0;
}
