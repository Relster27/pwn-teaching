#include <unistd.h>

char buf[16] = "AAAAAAAABBBBBBBB";
char something_crucial[16] = "pohon sawit";

int main(void)
{
        write(1, buf, 48); // reading past buffer
        return 0;
}
