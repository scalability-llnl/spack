# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Csdp(MakefilePackage):
    """CSDP is a library of routines that implements a predictor corrector
    variant of the semidefinite programming algorithm of Helmberg, Rendl,
    Vanderbei, and Wolkowicz"""

    homepage = "https://projects.coin-or.org/Csdp"
    url = "https://www.coin-or.org/download/source/Csdp/Csdp-6.1.1.tgz"

    license("CPL-1.0")

    version("6.1.1", sha256="0558a46ac534e846bf866b76a9a44e8a854d84558efa50988ffc092f99a138b9")

    depends_on("c", type="build")  # generated

    depends_on("atlas")

    def edit(self, spec, prefix):
        mkdirp(prefix.bin)
        makefile = FileFilter("Makefile")
        makefile.filter("/usr/local/bin", prefix.bin)
