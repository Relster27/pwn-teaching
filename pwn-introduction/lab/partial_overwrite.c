#include <stdio.h>

int main(void)
{
        char victim[8] = "secretzz";
        char buf[8] = {0};

        printf("victim before: %s\n", victim);
        read(0, buf, 10);
        printf("victim after : %s\n", victim);
        return 0;
}
