#!/bin/bash
echo "Script 14 starting......"
cd /dev/shm/shea9/tmp/spack-stage/spack-stage-zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/spack-src
ln -s libz.so.1.3.0.zlib-ng /dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/lib/libz.so
ln -s libz.so.1.3.0.zlib-ng /dev/shm/shea9/spack/opt/spack/linux-rhel8-icelake/gcc-10.3.1/zlib-ng-2.1.6-nafn5kmckv7cx4zyakpd5m2wyxemdnbn/lib/libz.so.1
(ldconfig || true)  >/dev/null 2>&1
echo "Script 14 done."
