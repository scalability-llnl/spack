# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AbseilCpp(CMakePackage):
    """Abseil Common Libraries (C++) """

    homepage = "https://abseil.io/"
    url      = "https://github.com/abseil/abseil-cpp/archive/20200923.2.tar.gz"

    maintainers = ['jcftang']

    version('20200923.2', sha256='bf3f13b13a0095d926b25640e060f7e13881bd8a792705dd9e161f3c2b9aa976')
    version('20200923.1', sha256='808350c4d7238315717749bab0067a1acd208023d41eaf0c7360f29cc8bc8f21')
    version('20200225.2', sha256='f41868f7a938605c92936230081175d1eae87f6ea2c248f41077c8f88316f111')
    version('20200225.1', sha256='0db0d26f43ba6806a8a3338da3e646bb581f0ca5359b3a201d8fb8e4752fd5f8')
    version('20190808', sha256='8100085dada279bf3ee00cd064d43b5f55e5d913be0dfe2906f06f8f28d5b37e')
    version('20181200', sha256='e2b53bfb685f5d4130b84c4f3050c81bf48c497614dc85d91dbd3ed9129bce6d')
    version('20180600', sha256='794d483dd9a19c43dc1fbbe284ce8956eb7f2600ef350dac4c602f9b4eb26e90')

    variant('shared', default=True,
            description='Build shared instead of static libraries')

    conflicts('+shared', when='@:20190808')

    def cmake_args(self):
        args = ["-DBUILD_TESTING=OFF",  "-DCMAKE_CXX_STANDARD=11"]
        args.append('-DBUILD_SHARED_LIBS:Bool={0}'.format(
            'ON' if '+shared' in self.spec else 'OFF'))
        return args
