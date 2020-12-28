# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nanoflann(CMakePackage):
    """a C++ header-only library for Nearest Neighbor (NN) search wih KD-trees.
    """

    homepage = "https://github.com/jlblancoc/nanoflann"
    url      = "https://github.com/jlblancoc/nanoflann/archive/v1.2.3.tar.gz"

    version('1.2.3', sha256='5ef4dfb23872379fe9eb306aabd19c9df4cae852b72a923af01aea5e8d7a59c3')

    def patch(self):
        filter_file('-mtune=native', '', 'CMakeLists.txt')

    def cmake_args(self):
        args = ['-DBUILD_SHARED_LIBS=ON']
        return args
