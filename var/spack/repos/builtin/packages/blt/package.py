# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Blt(Package):
    """BLT is a streamlined CMake-based foundation for Building, Linking and
       Testing large-scale high performance computing (HPC) applications."""

    homepage = "https://github.com/LLNL/blt"
    url      = "https://github.com/LLNL/blt/archive/v0.4.0.tar.gz"
    git      = "https://github.com/LLNL/blt.git"

    maintainers = ['white238', 'davidbeckingsale']

    version('develop', branch='develop')
    version('main', branch='main')
    version('0.4.0', sha256='f3bc45d28b9b2eb6df43b75d4f6f89a1557d73d012da7b75bac1be0574767193')
    version('0.3.6', sha256='6276317c29e7ff8524fbea47d9288ddb40ac06e9f9da5e878bf9011e2c99bf71')
    version('0.3.5', sha256='68a1c224bb9203461ae6f5ab0ff3c50b4a58dcce6c2d2799489a1811f425fb84')
    version('0.3.0', sha256='bb917a67cb7335d6721c997ba9c5dca70506006d7bba5e0e50033dd0836481a5')
    version('0.2.5', sha256='3a000f60194e47b3e5623cc528cbcaf88f7fea4d9620b3c7446ff6658dc582a5')
    version('0.2.0', sha256='c0cadf1269c2feb189e398a356e3c49170bc832df95e5564e32bdbb1eb0fa1b3')

    depends_on('cmake', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix)
