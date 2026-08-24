**``tcache demo:``**
- show difference 2.27 and 2.31 (before and after 'key' added)
- show how tcache_perthread_struct look like when there is a free happen
- demokan juga fungsi tcache_get() dan tcache_put() === basically tcache insertion and deletion

FILE: bin-demo/tcache.c & glibc-testing/2.27 & glibc-testing/2.31


**``fastbin demo:``**
- and show that 'key' isn't occur in fastbin
- tunjukin visualisasi main_arena->fastbinsY dan tunjukkin active entrynya yang ada 7
- tunjukin kalua entry di fastbin bisa muat lebih dari 7 chunk

FILE: bin-demo/fastbin.c


**``unsortedbin demo:``**
- demoin ketika chunk masuk unsortedbin, chunk yang masuk sizenya harus beda
- tunjukin letak chunknya di main_arena->bins

FILE: bin-demo/unsortedbin.c


**``smallbin demo:``**
- contohin demo di gdb bagaimana chunk fastbin/unsortedbin dilempar ke smallbin
- tunjukin letak chunknya di main_arena->bins

FILE: bin-demo/smallbin.c


**``largebin demo:``**
- contohin demo di gdb bagaimana chunk fastbin/unsortedbin dilempar ke largebin
- demoin juga isi dari entry di largebin (sizenya beda-beda)
- tunjukin letak chunknya di main_arena->bins

FILE: bin-demo/largebin.c & largebin_very-large.c


**``last remainder demo:``**
- demoin bagaimana last remainder terbentuk
- tunjukin letak chunknya di main_arena->bins

FILE: bin-demo/last_remainder.c


**``__malloc_hook demo:``**
- demoin gdb (set manually) of how hook behaves in version 2.27 and 2.36 (before and after hook removed)

FILE: glibc-testing/free_hook/out_2.31


**``pointer_guard & __exit_funcs demo:``**
- demokan lokasi pointer_guard (stack canary juga sekalian)
- relasi fsbase dan libc base
- demo di gdb metode pointer encryption dan demo juga di gdb (set manually) bagaimana __exit_funcs bekerja (sampe dapat shell)

FILE: glibc-testing/exit_funcs
