#include <stdio.h>
#include <unistd.h>

// gcc -o chall chall.c -no-pie -fno-stack-protector -z norelro -zexecstack -static

char name[0x80];

int main()
{
        setvbuf(stdin, 0, _IONBF, 0);
        setvbuf(stdout, 0, _IONBF, 0);

        char s[0x10];

        printf("Prepare your ROP gadget: ");
        read(0, name, 0x80);

        printf("Now pivot stack to name: ");
        read(0, s, 0x20);

        return 0;
}
