# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sparsehash(AutotoolsPackage):
    """Sparse and dense hash-tables for C++ by Google"""

    homepage = "https://github.com/sparsehash/sparsehash"
    url = "https://github.com/sparsehash/sparsehash/archive/sparsehash-2.0.4.tar.gz"

    license("BSD-3-Clause")

    version("2.0.4", sha256="8cd1a95827dfd8270927894eb77f62b4087735cbede953884647f16c521c7e58")
    version("2.0.3", sha256="05e986a5c7327796dad742182b2d10805a8d4f511ad090da0490f146c1ff7a8c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
