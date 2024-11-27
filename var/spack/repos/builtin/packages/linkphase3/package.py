# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Linkphase3(Package):
    """Haplotype reconstruction in pedigreed populations."""

    homepage = "https://github.com/tdruet/LINKPHASE3"
    git = "https://github.com/tdruet/LINKPHASE3.git"

    license("GPL-3.0-only")

    version("2017-06-14", commit="559913593fc818bb1adb29796a548cf5bf323827")

    depends_on("fortran", type="build")  # generated

    def install(self, spec, prefix):
        fortran = Executable(self.compiler.fc)
        fortran("LINKPHASE3.f90", "-o", "LINKPHASE3")
        mkdirp(prefix.bin)
        install("LINKPHASE3", prefix.bin)
