#include <stdio.h>
#include <stdlib.h>

long global_var_data = 0xdeadbeefcafebabe;
long global_var_bss_1 = 0x0;
long global_var_bss_2;

int add(int a, int b, int c)
{
        int local_add = a + b + c;
        return local_add;
}

int main(void)
{
        int res = add(0x27, 0x37, 0x47);
        printf("res: %d\n", res);

        char *heap = malloc(0x20);

        getchar();      // ini cuma untuk break doang
        return 0;
}
