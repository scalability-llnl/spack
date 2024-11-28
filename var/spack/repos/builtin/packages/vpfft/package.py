# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vpfft(MakefilePackage):
    """Proxy Application. VPFFT is an implementation of a mesoscale
    micromechanical materials model. By solving the viscoplasticity
    model, VPFFT simulates the evolution of a material under deformation.
    The solution time to the viscoplasticity model, described by a set
    of partial differential equations, is significantly reduced by the
    application of Fast Fourier Transform in the VPFFT algorithm.
    """

    homepage = "http://www.exmatex.org/vpfft.html"
    git = "https://github.com/exmatex/VPFFT.git"

    tag = ["proxy-app"]

    license("BSD-3-Clause")

    version("develop")

    depends_on("cxx", type="build")  # generated

    depends_on("eigen")
    depends_on("fftw")
    depends_on("mpi")

    @property
    def build_targets(self):
        targets = [
            "--file=Makefile.make",
            "EIGEN_PATH={0}".format(
                join_path(
                    self.spec["eigen"].prefix.include,
                    "eigen{0}".format(self.spec["eigen"].version.up_to(1)),
                )
            ),
            "FFTW_PATH={0}".format(self.spec["fftw"].prefix),
            "CC={0}".format(self.spec["mpi"].mpicxx),
        ]
        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("VPFFT++", prefix.bin)
        install("README.md", prefix)
        install("README.make", prefix)
        install("README-license.txt", prefix)
        install_tree("docs", prefix.docs)
