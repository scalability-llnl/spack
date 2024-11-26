# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dftd3Lib(MakefilePackage):
    """A dispersion correction for density functionals,
    Hartree-Fock and semi-empirical quantum chemical methods"""

    homepage = "https://www.chemie.uni-bonn.de/pctc/mulliken-center/software/dft-d3/dft-d3"
    url = "https://github.com/dftbplus/dftd3-lib/archive/0.9.2.tar.gz"

    version("0.10", sha256="db61bc6c7c699628e8c5bf2018ea38de03a53eac38014e06845829d765caf6bb")
    version("0.9.2", sha256="4178f3cf2f3e7e982a7084ec66bac92b4fdf164537d9fc0ada840a11b784f0e0")

    depends_on("fortran", type="build")  # generated

    # This fixes a concurrency bug, where make would try to start compiling
    # the dftd3 target before the lib target ended.
    # Since the library is small, disabling causes not much harm
    parallel = False

    def edit(self, spec, prefix):
        makefile = FileFilter("make.arch")
        makefile.filter("FC = gfortran", "")
        makefile.filter("LN = gfortran", "LN = $(FC)")

    def install(self, spec, prefix):
        mkdir(prefix.lib)
        mkdir(prefix.bin)
        mkdir(prefix.include)
        install("lib/libdftd3.a", prefix.lib)
        install("prg/dftd3", prefix.bin)
        install("lib/dftd3_api.mod", prefix.include)
        install("lib/dftd3_common.mod", prefix.include)
        install("lib/dftd3_core.mod", prefix.include)
        install("lib/dftd3_pars.mod", prefix.include)
        install("lib/dftd3_sizes.mod", prefix.include)
