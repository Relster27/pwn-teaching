#include <stdio.h>
#include <stdlib.h>

// Gak ada win() function :(

int main(void)
{
        char buf[16];
        fgets(buf, 64, stdin);
        return 0;
}

