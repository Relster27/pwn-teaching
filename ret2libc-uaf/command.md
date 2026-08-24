gdb:
to show source code of glibc:
        set substitute-path ./ /home/relster/tmp/junk/test/teach-demo/glibc-2.36/

to print all main_arena->bins entry:
        set $b = &main_arena.bins[0]
        set $i = 0
        while ($i < 254)
                printf "bin[%3d] fd=%p bk=%p\n", $i/2, $b[$i], $b[$i+1]
                set $i = $i + 2
        end
