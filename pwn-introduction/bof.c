#include <stdio.h>
#include <unistd.h>

int main(void)
{
        char buf[32];
        printf("Input: ");
        read(0, buf, 64);
        return 0;
}
