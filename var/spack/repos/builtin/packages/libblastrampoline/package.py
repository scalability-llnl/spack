# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libblastrampoline(MakefilePackage):
    """Using PLT trampolines to provide a BLAS and LAPACK demuxing library."""

    homepage = "https://github.com/staticfloat/libblastrampoline"
    git      = "https://github.com/staticfloat/libblastrampoline.git"

    version('3.0.2', commit='5882fdf6395afb1ed01a8a10db94b7b3cbd39e16')
    version('3.0.1', commit='e132e645db28bec024be9410467a6c7a2d0937ae')
    version('3.0.0', commit='7bb259a69e5bad0adb55171b2bee164a30ce2e91')
    version('2.2.0', commit='45f4a20ffdba5d368db66d71885312f5f73c2dc7')

    build_directory = 'src'

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make('prefix={0}'.format(prefix), 'install')
