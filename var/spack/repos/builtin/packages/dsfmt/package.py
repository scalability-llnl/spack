# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dsfmt(MakefilePackage):
    """Double precision SIMD-oriented Fast Mersenne Twister"""

    homepage = "http://www.math.sci.hiroshima-u.ac.jp/m-mat/MT/SFMT/"
    url = "https://github.com/MersenneTwister-Lab/dSFMT/archive/v2.2.4.tar.gz"

    maintainers("haampie")

    # This package does not have a target to build a library nor a make install target,
    # so we add it for them.
    patch("targets.patch")

    license("BSD-3-Clause")

    version("2.2.5", sha256="b7bc498cd140b4808963b1ff9f33b42a491870f54775c1060ecad0e02bcaffb4")
    version("2.2.4", sha256="39682961ecfba621a98dbb6610b6ae2b7d6add450d4f08d8d4edd0e10abd8174")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    @property
    def libs(self):
        return find_libraries("libdSFMT", root=self.prefix, recursive=True)

    def build(self, spec, prefix):
        make("build-library", "CC=cc")

    def install(self, spec, prefix):
        make("PREFIX={0}".format(prefix), "install")
