# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Msmc(MakefilePackage):
    """This software implements MSMC, a method to infer population size
    and gene flow from multiple genome sequences"""

    homepage = "https://github.com/stschiff/msmc"
    url = "https://github.com/stschiff/msmc/archive/v1.1.0.tar.gz"

    license("GPL-3.0-or-later")

    version("1.1.0", sha256="989064400fe392ca3d2ac1a253ce7edf1801b6a7eeb77bbf2ff7bf67910216c4")

    depends_on("gsl", type=("build", "run"))
    depends_on("dmd", type="build")

    def edit(self, spec, prefix):
        filter_file(
            "dmd", join_path(self.spec["dmd"].prefix.linux.bin64, "dmd"), "Makefile", string=True
        )

    def build(self, spec, prefix):
        gsllibdir = self.spec["gsl"].prefix.lib
        libgsl = join_path(gsllibdir, "libgsl.a")
        libgslcblas = join_path(gsllibdir, "libgslcblas.a")
        make("GSL={0} {1}".format(libgsl, libgslcblas))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree("build", prefix.bin)
