# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lemon(CMakePackage):
    """LEMON stands for Library for Efficient Modeling and Optimization in
    Networks. It is a C++ template library providing efficient implementations
    of common data structures and algorithms with focus on combinatorial
    optimization tasks connected mainly with graphs and networks."""

    homepage = "http://lemon.cs.elte.hu/trac/lemon"
    url      = "http://lemon.cs.elte.hu/pub/sources/lemon-1.3.1.tar.gz"

    version('1.3.1', sha256='71b7c725f4c0b4a8ccb92eb87b208701586cf7a96156ebd821ca3ed855bad3c8')
