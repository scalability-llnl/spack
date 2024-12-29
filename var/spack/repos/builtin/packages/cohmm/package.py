# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cohmm(MakefilePackage):
    """An anticipated important use-case for next-generation supercomputing
    is multiscale modeling, in which continuum equations for large-scale
    material deformation are augmented with high-fidelity, fine-scale
    simulations that provide constitutive data on demand.
    """

    tags = ["proxy-app"]

    homepage = "http://www.exmatex.org/cohmm.html"
    git = "https://github.com/exmatex/CoHMM.git"

    version("develop", branch="sad")

    depends_on("c", type="build")  # generated

    variant("openmp", default=True, description="Build with OpenMP Support")
    variant("gnuplot", default=False, description="Enable gnu plot Support")
    depends_on("gnuplot", when="+gnuplot")

    def edit(self, spec, prefix):
        if spec.satisfies("+openmp"):
            filter_file("DO_OPENMP = O.*", "DO_OPENMP = ON", "Makefile")
        if spec.satisfies("+gnuplot"):
            filter_file("DO_GNUPLOT = O.*", "DO_GNUPLOT = ON", "Makefile")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.input)
        mkdirp(prefix.doc)
        install("cohmm", prefix.bin)
        install("README.md", prefix.doc)
        install("LICENSE.md", prefix.doc)
        install("input/*.*", prefix.input)
