#include <stdio.h>

void print_name(char *nama_depan, char *nama_tengah, char *nama_belakang)
{
        printf("%s %s %s\n", nama_depan, nama_tengah, nama_belakang);
}

int main(void)
{
        char *nama_depan = "Claire";
        char *nama_tengah = "Violet";
        char *nama_belakang = "Lanaya";
        print_name(nama_depan, nama_tengah, nama_belakang);
        return 0;
}
