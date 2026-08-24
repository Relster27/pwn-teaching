#include <stdio.h>
#include <unistd.h>

/*
    OOB Write global variable to trigger win function.
*/

typedef unsigned long long u64;

u64 fingerprint = 0xf4f4f4f4f4f4f4f4;
u64 ids[4];

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
        printf("[AUTHENTICATED] %s\n", flag_buf);
        fclose(flag_fd);
}

void vuln(void) {
    printf("Please input index > ");
    int idx = -1;
    scanf("%d", &idx);

    printf("Please input your fingerprint ID > ");
    u64 id = -1;
    scanf("%llu", &id);

    if (idx > 3) {
        puts("[ABORT] Such index not allowed.");
        _exit(1);
    }
    
    ids[idx] = id;

    if (fingerprint != 0xfadebabed00df00d) {
        puts("[UNAUTHENTICAED] Fingerprint doesn't match.");
        _exit(0);
    } else {
        win();
    }
}

int main(void) {
    vuln();
    return 0;
}
