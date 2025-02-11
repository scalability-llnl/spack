#!/bin/bash
echo "Script 20 Starting."
export CMAKE_PREFIX_PATH=/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn:/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/gmake-4.4.1-h4caimdpmzjqeyrfqjwkkivkrij43g67:/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/gcc-runtime-10.3.1-avimx2fhnnncfj3rpmaqatprvc2ou4yx;
export PATH=/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/gmake-4.4.1-h4caimdpmzjqeyrfqjwkkivkrij43g67/bin:/dev/shm/shea9/spack/lib/spack/env/gcc:/dev/shm/shea9/spack/lib/spack/env/case-insensitive:/dev/shm/shea9/spack/lib/spack/env:/dev/shm/shea9/spack/bin:/usr/tce/packages/python/python-3.10.8/bin:/usr/tce/packages/texlive/texlive-20220321/bin/x86_64-linux:/usr/tce/packages/texlive/texlive-20220321/bin:/usr/global/tools/jobutils/bin:/usr/tce/packages/mvapich2/mvapich2-2.3.7-intel-classic-2021.6.0-magic/bin:/usr/tce/packages/intel-classic/intel-classic-2021.6.0-magic/bin:/usr/tce/bin:/usr/lib64/ccache:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:.;
export PKG_CONFIG_PATH=/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/lib/pkgconfig:/usr/tce/packages/texlive/texlive-20220321/lib/pkgconfig;
export SPACK_DEBUG_LOG_DIR=/dev/shm/shea9/spack/share/spack;
export SPACK_DEBUG_LOG_ID=pigz-64f5mnl;
export SPACK_SHORT_SPEC="pigz@2.8%gcc@10.3.1 build_system=makefile arch=linux-rhel8-icelake/64f5mnl";
export SPACK_STORE_INCLUDE_DIRS=/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/include;
export SPACK_STORE_LINK_DIRS=/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/lib:/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/gcc-runtime-10.3.1-avimx2fhnnncfj3rpmaqatprvc2ou4yx/lib;
export SPACK_STORE_RPATH_DIRS=/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/pigz-2.8-64f5mnl2bfwvzv56oa77vyk2liw7uhoj/lib:/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/pigz-2.8-64f5mnl2bfwvzv56oa77vyk2liw7uhoj/lib64:/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/lib:/dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/gcc-runtime-10.3.1-avimx2fhnnncfj3rpmaqatprvc2ou4yx/lib;
cd /dev/shm/shea9/tmp/spack-stage/spack-stage-pigz-2.8-64f5mnl2bfwvzv56oa77vyk2liw7uhoj/spack-src
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
echo "Script 20 done."
