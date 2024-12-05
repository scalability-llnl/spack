# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Filtlong(MakefilePackage):
    """Filtlong is a tool for filtering long reads by quality. It can
    take a set of long reads and produce a smaller, better subset."""

    homepage = "https://github.com/rrwick/Filtlong"
    url = "https://github.com/rrwick/Filtlong/archive/v0.2.0.tar.gz"

    license("GPL-3.0-only")

    version("0.2.1", sha256="e6f47675e87f98cf2481a60bef5cad38396f1e4db653a5c1673139f37770273a")
    version("0.2.0", sha256="a4afb925d7ced8d083be12ca58911bb16d5348754e7c2f6431127138338ee02a")
    version("0.1.1", sha256="ddae7a5850efeb64424965a443540b1ced34286fbefad9230ab71f4af314081b")

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")

    # %gcc@13: requires std libraries be manually added - add an include for `cstdint`
    patch("gcc13.patch", level=0, when="%gcc@13:")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install_tree("bin", prefix.bin)

        mkdir(prefix.test)
        install_tree("test", prefix.test)
