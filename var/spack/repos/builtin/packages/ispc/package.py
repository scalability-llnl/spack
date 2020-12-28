# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


# ispc requires <gnu/stubs-32.h>, e.g. from
# glibc-devel.i686 (CentoOS) or libc6-dev-i386 and g++-multilib (Ubuntu)


import re

from spack.package import *


class Ispc(CMakePackage):
    """Intel Implicit SPMD Program Compiler

    An open-source compiler for high-performance SIMD programming on the CPU"""

    homepage = "https://ispc.github.io"
    url      = "https://github.com/ispc/ispc/tarball/v1.14.1"
    git      = "https://github.com/ispc/ispc"
    maintainers = ['aumuell']

    executables = ['^ispc$']

    version('master', branch='master')
    version('1.14.1', sha256='ca12f26dafbc4ef9605487d03a2156331c1351a4ffefc9bab4d896a466880794')
    version('1.14.0', sha256='1ed72542f56738c632bb02fb0dd56ad8aec3e2487839ebbc0def8334f305a4c7')
    version('1.13.0', sha256='aca595508b51dd1ff065c406a3fd7c93822320c510077dd4d97a2b98a23f097a')

    depends_on('python', type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('ncurses', type='link')
    depends_on('zlib', type='link')
    depends_on('llvm~libcxx')
    depends_on('llvm@10:', when='@1.14:')
    depends_on('llvm@10:10.999', when='@1.13:1.13.999')

    patch('don-t-assume-that-ncurses-zlib-are-system-libraries.patch',
          when='@1.14:1.14.999',
          sha256='d3ccf547d3ba59779fd375e10417a436318f2200d160febb9f830a26f0daefdc')

    patch('fix-linking-against-llvm-10.patch', when='@1.13:1.13.999',
          sha256='d3ccf547d3ba59779fd375e10417a436318f2200d160febb9f830a26f0daefdc')

    def cmake_args(self):
        args = []
        args.append('-DARM_ENABLED=FALSE')
        args.append('-DISPC_NO_DUMPS=ON')  # otherwise, LLVM needs patching
        args.append('-DISPC_INCLUDE_EXAMPLES=OFF')
        args.append('-DISPC_INCLUDE_TESTS=OFF')
        args.append('-DISPC_INCLUDE_UTILS=OFF')
        return args

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'^Intel.*[iI][sS][pP][cC]\),\s+(\S+)\s+\(build.*\)',
                          output)
        return match.group(1) if match else None
