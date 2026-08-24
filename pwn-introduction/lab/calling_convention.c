#include <stdio.h>

long long add(int a, int b, int c, int d, int e, int f)
{
        return a + b + c + d + e + f;
}

int main(void)
{
        long long res = add(0x13, 0x69, 0x27, 0x67, 0x420, 0x1337);    
        return 0;
}
