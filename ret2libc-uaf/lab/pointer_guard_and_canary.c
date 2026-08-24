// pg_threads_canary.c
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <pthread.h>
#include <unistd.h>

static inline uint64_t read_pointer_guard() {
    uint64_t val;
    __asm__("mov %%fs:0x30, %0" : "=r"(val));
    return val;
}

static inline uint64_t read_stack_canary() {
    uint64_t val;
    __asm__("mov %%fs:0x28, %0" : "=r"(val));
    return val;
}

void* thread_func(void* arg) {
    long id = (long)arg;

    uint64_t guard  = read_pointer_guard();
    uint64_t canary = read_stack_canary();

    printf("[Thread %ld] pointer_guard = 0x%lx | stack_canary = 0x%lx\n",
           id, guard, canary);

    pause();   // keep thread alive for GDB
    return NULL;
}

int main() {
    pthread_t t1, t2;

    printf("[Main]     pointer_guard = 0x%lx | stack_canary = 0x%lx\n",
           read_pointer_guard(), read_stack_canary());

    pthread_create(&t1, NULL, thread_func, (void*)1);
    pthread_create(&t2, NULL, thread_func, (void*)2);

    pause();   // keep main alive
    return 0;
}
