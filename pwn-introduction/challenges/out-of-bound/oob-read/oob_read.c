#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

/*
    OOB Read flag value on global variable.
*/

char flag[] = "FLAG{XXXXXXXXXXXXXXXXXXXXXXXXXXXX}";     // data
char global_buf[64] = {0};                              // bss

__attribute__((constructor)) void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

__attribute__((constructor)) void copy_flag(void) {
    FILE *flag_fd = fopen("./flag.txt", "r");
    if (flag_fd == NULL) {
        perror("fopen");
        _exit(1);
    }
    char flag_buf[64] = {0};
    fgets(flag_buf, sizeof(flag_buf), flag_fd);
    strcpy(flag, flag_buf);
    fclose(flag_fd);
}

__attribute__((constructor)) void fill_global_buf(void) {
    srand(time(NULL));

    for (int i = 0; i < sizeof(global_buf); i++) {
        char min_char = ' '; // Space (ASCII 32)
        char max_char = '~'; // Tilde (ASCII 126)
        int random_value = rand();
        global_buf[i] = (random_value % (max_char - min_char + 1)) + min_char;
    }    
    global_buf[sizeof(global_buf) - 1] = '\0'; 
}

int main(void) {

    while (1) {
        printf("Input your index: ");
        int idx = 0;
        scanf("%d", &idx); getchar();

        printf("Strings: ");
        for (int i = 0; i < 10; i++) {
            printf("%c", global_buf[idx++]);
        }
        puts("");
    }

    // index = -130 -120 -110 -100

    return 0;
}
