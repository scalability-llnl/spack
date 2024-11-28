# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libtommath(MakefilePackage):
    """A portable number theoretic multiple-precision integer library."""

    homepage = "https://www.libtom.net/"
    url = "https://github.com/libtom/libtommath/archive/v1.2.0.tar.gz"

    license("Unlicense")

    version("1.3.0", sha256="6d099e93ff00fa9b18346f4bcd97dcc48c3e91286f7e16c4ac5515a7171c3149")
    version("1.2.1", sha256="068adaf5155d28d4ac976eb95ea0df1ecb362f20d777287154c22a24fdb35faa")
    version("1.2.0", sha256="f3c20ab5df600d8d89e054d096c116417197827d12732e678525667aa724e30f")
    version("1.1.0", sha256="71b6f3f99341b7693393ab4b58f03b79b6afc2ee5288666cc4538b4b336355f4")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        make(f"DESTDIR={prefix}", "LIBPATH=/lib", "INCPATH=/include", "install")
