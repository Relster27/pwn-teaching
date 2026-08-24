#include <stdio.h>
#include <string.h>
// gcc -no-pie -fno-stack-protector -z execstack -g -o chal chal.c

__attribute__((constructor))
void init(void)
{
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

int main() {
    char buffer1[64];

    printf("The buffer is located at: %p\n", buffer1);

    printf("Shellcode: ");
    gets(buffer1);
}
