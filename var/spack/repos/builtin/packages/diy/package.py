# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Diy(CMakePackage):
    """Data-parallel out-of-core library"""

    homepage = "https://github.com/diatomic/diy"
    url      = "https://github.com/diatomic/diy/archive/3.5.0.tar.gz"
    git      = "https://github.com/diatomic/diy.git"

    version('3.5.0', sha256='b3b5490441d521b6e9b33471c782948194bf95c7c3df3eb97bc5cf4530b91576')
    version('master', branch='master')

    depends_on('mpi')

    def cmake_args(self):
        args = ['-Dbuild_examples=off',
                '-Dbuild_tests=off',
                '-DCMAKE_CXX_COMPILER=%s' % self.spec['mpi'].mpicxx]
        return args
