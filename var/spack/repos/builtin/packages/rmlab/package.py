# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rmlab(CMakePackage):
    """C++ File API for the reMarkable tablet"""

    homepage = "https://github.com/ax3l/lines-are-beautiful"
    git      = "https://github.com/ax3l/lines-are-beautiful.git"

    maintainers = ['ax3l']

    version('develop', branch='develop')

    variant('png', default=True,
            description='Enable PNG conversion support')

    # modern CMake
    depends_on('cmake@3.7.0:', type='build')
    # C++11
    conflicts('%gcc@:4.7')
    conflicts('%intel@:15')
    conflicts('%pgi@:14')

    depends_on('pngwriter@0.6.0:', when='+png')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DRmlab_USE_PNG={0}'.format(
                'ON' if '+png' in spec else 'OFF')
        ]
        return args
