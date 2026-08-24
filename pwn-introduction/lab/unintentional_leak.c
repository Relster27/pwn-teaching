#include <stdio.h>
#include <unistd.h>

int main(void)
{
        char secret[24] = "INDONESIA EMAS 2067";
        char buf[16] = {0};
        read(0, buf, 16);

        printf("your input: %s\n", buf); // Unintentionally leak data
        return 0;
}
