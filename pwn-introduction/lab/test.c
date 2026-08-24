#include <stdio.h>
#include <string.h>
#include <stdlib.h>

__attribute__((constructor)) void init(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(void) {

    char buf[0x20];
    printf("> ");
    gets(buf);

    return 0;
}