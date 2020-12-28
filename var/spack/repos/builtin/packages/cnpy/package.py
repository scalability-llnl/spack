# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Cnpy(CMakePackage):
    """cnpy: library to read/write .npy and .npz files in C/C++."""

    homepage = "https://github.com/rogersce/cnpy"
    git      = "https://github.com/rogersce/cnpy.git"

    version('master', branch='master')

    depends_on('zlib', type='link')

    def cmake_args(self):
        args = []
        if sys.platform == 'darwin':
            args.extend(['-DCMAKE_MACOSX_RPATH=ON'])

        return args
