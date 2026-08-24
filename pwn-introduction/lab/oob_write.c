#include <stdio.h>
#include <string.h>

char buf[16] = "AAAAAAAABBBB";
char victim[16] = "admin#1234";

int main(void)
{

        printf("victim before: %s\n", victim);
        
        memset(buf, 0x67, 32);  // writing past buffer
        
        printf("victim after : %s\n", victim);
        return 0;
}
