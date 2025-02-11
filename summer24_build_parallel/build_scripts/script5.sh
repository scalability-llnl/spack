#!/bin/bash
echo "Script 5 starting......"
cd /dev/shm/shea9/tmp/spack-stage/spack-stage-zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/spack-src
cp arch/x86/adler32_avx512_vnni.lo adler32_avx512_vnni.lo
#make[1]: Leaving directory '/dev/shm/shea9/tmp/spack-stage/spack-stage-zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/spack-src/arch/x86'
cp arch/x86/slide_hash_sse2.lo slide_hash_sse2.lo
#make[1]: Leaving directory '/dev/shm/shea9/tmp/spack-stage/spack-stage-zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/spack-src/arch/x86'
cp arch/x86/compare256_avx2.lo compare256_avx2.lo
/dev/shm/shea9/spack/lib/spack/env/gcc/gcc -O2  -std=c11 -Wall -DNDEBUG -DHAVE_SYMVER -D_LARGEFILE64_SOURCE=1 -DHAVE_POSIX_MEMALIGN -DHAVE_ALIGNED_ALLOC -DHAVE_SYS_AUXV_H -DZLIB_COMPAT -DWITH_GZFILEOP -DHAVE_VISIBILITY_HIDDEN -DHAVE_VISIBILITY_INTERNAL -DHAVE_ATTRIBUTE_ALIGNED -DHAVE_BUILTIN_CTZ -DHAVE_BUILTIN_CTZLL -DX86_FEATURES -DX86_AVX2 -DX86_AVX512 -DX86_MASK_INTRIN -DX86_AVX512VNNI -DX86_SSE42 -DX86_SSE2 -DX86_SSSE3 -DX86_PCLMULQDQ_CRC -DX86_VPCLMULQDQ_CRC  -o example example.o  libz.a 
/dev/shm/shea9/spack/lib/spack/env/gcc/gcc -O2  -std=c11 -Wall -DNDEBUG -DHAVE_SYMVER -D_LARGEFILE64_SOURCE=1 -DHAVE_POSIX_MEMALIGN -DHAVE_ALIGNED_ALLOC -DHAVE_SYS_AUXV_H -DZLIB_COMPAT -DWITH_GZFILEOP -DHAVE_VISIBILITY_HIDDEN -DHAVE_VISIBILITY_INTERNAL -DHAVE_ATTRIBUTE_ALIGNED -DHAVE_BUILTIN_CTZ -DHAVE_BUILTIN_CTZLL -DX86_FEATURES -DX86_AVX2 -DX86_AVX512 -DX86_MASK_INTRIN -DX86_AVX512VNNI -DX86_SSE42 -DX86_SSE2 -DX86_SSSE3 -DX86_PCLMULQDQ_CRC -DX86_VPCLMULQDQ_CRC  -o minigzip minigzip.o  libz.a 
/dev/shm/shea9/spack/lib/spack/env/gcc/gcc -O2  -std=c11 -Wall -DNDEBUG -DHAVE_SYMVER -D_LARGEFILE64_SOURCE=1 -DHAVE_POSIX_MEMALIGN -DHAVE_ALIGNED_ALLOC -DHAVE_SYS_AUXV_H -DZLIB_COMPAT -DWITH_GZFILEOP -DHAVE_VISIBILITY_HIDDEN -DHAVE_VISIBILITY_INTERNAL -DHAVE_ATTRIBUTE_ALIGNED -DHAVE_BUILTIN_CTZ -DHAVE_BUILTIN_CTZLL -DX86_FEATURES -DX86_AVX2 -DX86_AVX512 -DX86_MASK_INTRIN -DX86_AVX512VNNI -DX86_SSE42 -DX86_SSE2 -DX86_SSSE3 -DX86_PCLMULQDQ_CRC -DX86_VPCLMULQDQ_CRC  -o makefixed makefixed.o libz.a 
/dev/shm/shea9/spack/lib/spack/env/gcc/gcc -O2  -std=c11 -Wall -DNDEBUG -DHAVE_SYMVER -D_LARGEFILE64_SOURCE=1 -DHAVE_POSIX_MEMALIGN -DHAVE_ALIGNED_ALLOC -DHAVE_SYS_AUXV_H -DZLIB_COMPAT -DWITH_GZFILEOP -DHAVE_VISIBILITY_HIDDEN -DHAVE_VISIBILITY_INTERNAL -DHAVE_ATTRIBUTE_ALIGNED -DHAVE_BUILTIN_CTZ -DHAVE_BUILTIN_CTZLL -DX86_FEATURES -DX86_AVX2 -DX86_AVX512 -DX86_MASK_INTRIN -DX86_AVX512VNNI -DX86_SSE42 -DX86_SSE2 -DX86_SSSE3 -DX86_PCLMULQDQ_CRC -DX86_VPCLMULQDQ_CRC  -o maketrees maketrees.o libz.a 
/dev/shm/shea9/spack/lib/spack/env/gcc/gcc -O2  -std=c11 -Wall -DNDEBUG -DHAVE_SYMVER -D_LARGEFILE64_SOURCE=1 -DHAVE_POSIX_MEMALIGN -DHAVE_ALIGNED_ALLOC -DHAVE_SYS_AUXV_H -DZLIB_COMPAT -DWITH_GZFILEOP -DHAVE_VISIBILITY_HIDDEN -DHAVE_VISIBILITY_INTERNAL -DHAVE_ATTRIBUTE_ALIGNED -DHAVE_BUILTIN_CTZ -DHAVE_BUILTIN_CTZLL -DX86_FEATURES -DX86_AVX2 -DX86_AVX512 -DX86_MASK_INTRIN -DX86_AVX512VNNI -DX86_SSE42 -DX86_SSE2 -DX86_SSSE3 -DX86_PCLMULQDQ_CRC -DX86_VPCLMULQDQ_CRC  -o makecrct makecrct.o libz.a 
#make[1]: Leaving directory '/dev/shm/shea9/tmp/spack-stage/spack-stage-zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/spack-src/arch/x86'
cp arch/x86/chunkset_avx2.lo chunkset_avx2.lo
#make[1]: Leaving directory '/dev/shm/shea9/tmp/spack-stage/spack-stage-zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/spack-src/arch/x86'
cp arch/x86/chunkset_sse2.lo chunkset_sse2.lo
#make[1]: Leaving directory '/dev/shm/shea9/tmp/spack-stage/spack-stage-zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/spack-src/arch/x86'
cp arch/x86/adler32_ssse3.lo adler32_ssse3.lo
#make[1]: Leaving directory '/dev/shm/shea9/tmp/spack-stage/spack-stage-zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/spack-src/arch/x86'
cp arch/x86/crc32_pclmulqdq.lo crc32_pclmulqdq.lo
#make[1]: Leaving directory '/dev/shm/shea9/tmp/spack-stage/spack-stage-zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/spack-src/arch/x86'
cp arch/x86/chunkset_ssse3.lo chunkset_ssse3.lo
#make[1]: Leaving directory '/dev/shm/shea9/tmp/spack-stage/spack-stage-zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/spack-src/arch/x86'
cp arch/x86/crc32_vpclmulqdq.lo crc32_vpclmulqdq.lo
echo "Script 5 done."
