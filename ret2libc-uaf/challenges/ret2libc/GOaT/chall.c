#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// Vuln: OOB -> GOT Overwrite -> Ret2libc -> strcmp("/bin/sh") (first arg is user controlled string)

// Compilation: gcc vuln.c -o vuln -no-pie -fno-stack-protector -Wl,-z,lazy

char *dead;
char *secret;
long long data[10];

void setup()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

int main(void)
{
        size_t menu_idx;
        long long value;
        secret = (char*)&dead;

        setup();

        printf("Welcome to the Secure Note Portal.\n");
        printf("For you <3: %p\n", (void*)wctomb);

        while(1) {
                printf("\n1. Write Data\n2. Exit\n> ");
                if (scanf("%llu", &menu_idx) != 1) break;

                if (menu_idx == 1) {
                        printf("Enter index: ");
                        int idx;
                        scanf("%d", &idx); 

                        printf("Enter value (hex): ");
                        scanf("%llx", &value);
                        
                        data[idx] = value;
                        printf("Data updated.\n");
                } 
                else if (menu_idx == 2) {
                        if (strcmp(secret, "exit") == 0) {
                                printf("Goodbye!\n");
                                exit(0);
                        }
                } else {
                        puts("Invalid menu");
                }
        }

        return 0;
}
