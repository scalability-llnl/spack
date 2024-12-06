# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GtkorvoDill(CMakePackage):
    """DILL provides instruction-level code generation,
    register allocation and simple optimizations for generating
    executable code directly into memory regions for immediate use.
    """

    homepage = "https://github.com/GTkorvo/dill"
    url = "https://github.com/GTkorvo/dill/archive/v2.1.tar.gz"
    git = "https://github.com/GTkorvo/dill.git"

    version("develop", branch="master")
    version("2.4", sha256="ed7745d13e8c6a556f324dcc0e48a807fc993bdd5bb1daa94c1df116cb7e81fa")
    version("2.1", sha256="7671e1f3c25ac6a4ec2320cec2c342a2f668efb170e3dba186718ed17d2cf084")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Ref: https://github.com/GTkorvo/dill/commit/dac6dfcc7fdaceeb4c157f9ecdf5ecc28f20477f
    patch("2.4-fix-clear_cache.patch", when="@2.4")
    patch("2.1-fix-clear_cache.patch", when="@2.1")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("@2.4:"):
            args.append("-DBUILD_SHARED_LIBS=OFF")
        else:
            args.append("-DENABLE_BUILD_STATIC=STATIC")

        if self.run_tests:
            args.append("-DENABLE_TESTING=1")
        else:
            args.append("-DENABLE_TESTING=0")

        return args
