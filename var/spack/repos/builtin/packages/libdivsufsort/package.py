# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libdivsufsort(CMakePackage):
    """libdivsufsort is a software library that implements a
     lightweight suffix array construction algorithm."""

    homepage = "https://github.com/y-256/libdivsufsort"
    url      = "https://github.com/y-256/libdivsufsort/archive/2.0.1.tar.gz"

    version('2.0.1', sha256='9164cb6044dcb6e430555721e3318d5a8f38871c2da9fd9256665746a69351e0')

    def cmake_args(self):
        args = ['-DBUILD_DIVSUFSORT64=ON']
        return args
