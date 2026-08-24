#include <stdio.h>
#include <unistd.h>

/*
    Buffer overflow to win function.
*/

__attribute__((constructor)) void init(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win(void)
{
    FILE *flag_fd = fopen("./flag.txt", "r");
    if (flag_fd == NULL) {
        perror("fopen");
        _exit(1);
    }

    char flag_buf[64] = {0};
    fgets(flag_buf, sizeof(flag_buf), flag_fd);
    printf("\nHere's your flag: %s\n", flag_buf);
    fclose(flag_fd);
}

void vuln(void)
{
    char buf[32] = {0};
    printf("Input: ");
    fgets(buf, 64, stdin);
}

int main(void) {

    puts("There's a win function, go get the flag!!");
    vuln();

    return 0;
}
