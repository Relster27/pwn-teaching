#include <stdio.h>
#include <stdlib.h>

long globalz = 0x6767676769696969;

void something(void)
{
        long local_something = 0x4141414142424242;
}

int main(void)
{
        long local_main = 0xdeadbeefcafebabe;
        char *heap = malloc(0x10);
        something();
        return;
}