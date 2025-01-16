#!/bin/bash
echo "Script 21 Starting....."
cd /dev/shm/shea9/tmp/spack-stage/spack-stage-pigz-2.8-64f5mnl2bfwvzv56oa77vyk2liw7uhoj/spack-src
cc  -o pigz pigz.o yarn.o try.o deflate.o blocksplitter.o tree.o lz77.o cache.o hash.o util.o squeeze.o katajainen.o symbols.o -lm -lpthread -lz
echo "Script 21 done."
