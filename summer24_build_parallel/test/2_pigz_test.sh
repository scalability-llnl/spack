#!/bin/bash
cd /dev/shm/shea9/tmp/spack-stage/spack-stage-pigz-2.8-64f5mnl2bfwvzv56oa77vyk2liw7uhoj/spack-src
echo "pigz test commands beginning"
cc -O3 -Wall   -c -o pigz.o pigz.c
cc -O3 -Wall   -c -o yarn.o yarn.c #no dependency on line above it, could be run at the same time on different cores
cc -O3 -Wall   -c -o try.o try.c
cc -O3 -Wall -c zopfli/src/zopfli/deflate.c #recognize that this implicitly creates deflate.o (based on the -c)
cc -O3 -Wall -c zopfli/src/zopfli/blocksplitter.c 
cc -O3 -Wall -c zopfli/src/zopfli/tree.c
cc -O3 -Wall -c zopfli/src/zopfli/lz77.c
cc -O3 -Wall -c zopfli/src/zopfli/cache.c
cc -O3 -Wall -c zopfli/src/zopfli/hash.c
cc -O3 -Wall -c zopfli/src/zopfli/util.c
cc -O3 -Wall -c zopfli/src/zopfli/squeeze.c
cc -O3 -Wall -c zopfli/src/zopfli/katajainen.c
cc -O3 -Wall -c zopfli/src/zopfli/symbols.c
echo "pigz test commands done"
