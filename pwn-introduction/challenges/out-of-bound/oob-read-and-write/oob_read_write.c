#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/*
    OOB Read-Write to win function.
*/

typedef unsigned long long u64;

__attribute__((constructor)) void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win(void) {
        FILE *flag_fd = fopen("./flag.txt", "r");
        if (flag_fd == NULL) {
            perror("fopen");
            _exit(1);
        }
        char flag_buf[64] = {0};
        fgets(flag_buf, sizeof(flag_buf), flag_fd);
        printf("Leaked information: %s\n", flag_buf);
        fclose(flag_fd);
}

void vuln(void) {
    u64 data[32];
    data[0] = 0x4141414141414141;
    data[1] = 0x4242424242424242;
    data[30] = 0x4343434343434343;
    data[31] = 0x4444444444444444;
    
    u64 idx = -1;
    printf("Index to read > ");
    scanf("%llu", &idx);
    printf("Value: 0x%llx\n", data[idx]);

    printf("Index to write > ");
    scanf("%llu", &idx);
    printf("Value > ");
    scanf("%llu", &data[idx]);
    
    return;
}

int main(void) {
    // printf("win: %lld\n", win); // disable this
    vuln();
    return 0;
}
