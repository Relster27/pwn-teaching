#include <stdio.h>

int main(void)
{
        printf("Here's intentional leak: %p\n", &main);
        return 0;
}
