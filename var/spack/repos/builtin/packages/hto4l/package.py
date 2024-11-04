# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hto4l(MakefilePackage):
    """Hto4l is an event generator for the SM Higgs decay into 4 charged leptons
    up to NLOPS electroweak accuracy and in presence of dimension-6 operators."""

    homepage = "https://www2.pv.infn.it/~hepcomplex/hto4l.html"
    url = "https://www2.pv.infn.it/hepcomplex/releases/hto4l/Hto4l-v2.02.tar.bz2"

    maintainers("haralmha")

    version("2.02", sha256="1a7061689ddaf6bde1f12032479c529a9787d7b038ed55a0325398bd531aadf6")

    depends_on("gsl")

    @when("@2.02")
    def patch(self):
        filter_file(
            r"FFLAGS =  -O1 -g -ffixed-line-length-none     "
            + r"-fno-range-check  \$\(DEF\)QUAD=0 \$\(DEF\)U77EXT=0",
            "FFLAGS =  -O1 -g -ffixed-line-length-none -std=legacy "
            + "-fno-range-check  $(DEF)QUAD=0 $(DEF)U77EXT=0",
            "LoopTools-2.10/makefile-lxplus",
        )
        filter_file(
            r"-mkdir \$\(PREFIX\)", "-mkdir -p $(PREFIX)", "LoopTools-2.10/makefile-lxplus"
        )
        filter_file(
            r"-mkdir \$\(LIBDIR\) \$\(BINDIR\) \$\(INCLUDEDIR\)",
            "-mkdir -p $(LIBDIR) $(BINDIR) $(INCLUDEDIR)",
            "LoopTools-2.10/makefile-lxplus",
        )

    def edit(self, spec, prefix):
        env["GSL_HOME"] = self.spec["gsl"].prefix

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("Hto4l", prefix.bin)
