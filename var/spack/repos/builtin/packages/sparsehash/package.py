# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sparsehash(AutotoolsPackage):
    """Sparse and dense hash-tables for C++ by Google"""
    homepage = "https://github.com/sparsehash/sparsehash"
    url      = "https://github.com/sparsehash/sparsehash/archive/sparsehash-2.0.3.tar.gz"

    version('2.0.3', sha256='05e986a5c7327796dad742182b2d10805a8d4f511ad090da0490f146c1ff7a8c')
