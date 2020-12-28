# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Thrust(Package):
    """Thrust is a parallel algorithms library
    which resembles the C++ Standard Template Library (STL)."""

    homepage = "https://thrust.github.io"
    url      = "https://github.com/thrust/thrust/archive/1.9.4.tar.gz"

    version('1.9.4', sha256='41931a7d73331fc39c6bea56d1eb8d4d8bbf7c73688979bbdab0e55772f538d1')
    version('1.9.3', sha256='92482ad0219cd2d727766f42a4fc952d7c5fd0183c5e201d9a117568387b4fd1')
    version('1.9.2', sha256='1fb1272be9e8c28973f5c39eb230d1914375ef38bcaacf09a3fa51c6b710b756')
    version('1.9.1', sha256='7cf59bf42a7b05bc6799c88269bf41eb637ca2897726a5ade334a1b8b4579ef1')
    version('1.9.0', sha256='a98cf59fc145dd161471291d4816f399b809eb0db2f7085acc7e3ebc06558b37')
    version('1.8.3', sha256='2254200512fde7f4fd0fc74306286e192ea6ac9037576dbd31309c0579229dbb')
    version('1.8.2', sha256='83bc9e7b769daa04324c986eeaf48fcb53c2dda26bcc77cb3c07f4b1c359feb8')

    def install(self, spec, prefix):
        install_tree('doc', join_path(prefix, 'doc'))
        install_tree('examples', join_path(prefix, 'examples'))
        install_tree('thrust', join_path(prefix, 'include', 'thrust'))
