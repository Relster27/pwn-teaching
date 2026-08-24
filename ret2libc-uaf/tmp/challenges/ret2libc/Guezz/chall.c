#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dlfcn.h>
#include <unistd.h>

void vuln() {
        char buf[64];
        printf("Input your guess: ");
        read(0, buf, 256);
}

int main() {
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);

        char name[128];

        puts("=== Libc Oracle ===");
        puts("Type function name to leak its address.");
        puts("Type 'guezz' when you are ready.");

        while (1) {
                printf("> ");
                fgets(name, sizeof(name), stdin);
                name[strcspn(name, "\n")] = 0;

                if (strcmp(name, "guezz") == 0)
                        break;

                void *addr = dlsym(RTLD_DEFAULT, name);
                if (addr)
                        printf("%s @ %p\n", name, addr);
                else
                        puts("Not found.");
        }

        vuln();
        return 0;
}
