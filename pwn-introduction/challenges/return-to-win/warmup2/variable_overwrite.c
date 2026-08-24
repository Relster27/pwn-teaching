#include <stdio.h>
#include <stdlib.h>

#define TARGET 0xdeadbeefcafebabe

__attribute__((constructor))
void init(void)
{
	setbuf(stdout, NULL);
	setbuf(stdin, NULL);
	setbuf(stderr, NULL);
}

int main(void)
{
	long overwrite_me = 0;
	char buf[64] = {0};

	printf("Input: ");
	gets(buf);	// vulnerable

	if (overwrite_me == TARGET) {
		printf("overwrite_me == 0x%llx\n", TARGET);
		system("cat flag.txt");
	} else {
		printf("overwrite_me == 0x%llx\n", overwrite_me);
		printf("overwrite_me != 0x%llx\n", TARGET);
	} 

	return 0;
}
