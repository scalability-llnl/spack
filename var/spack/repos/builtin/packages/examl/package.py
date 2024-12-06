# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Examl(MakefilePackage):
    """
    Exascale Maximum Likelihood (ExaML) code for phylogenetic inference
    using MPI. This code implements the popular RAxML search algorithm
    for maximum likelihood based inference of phylogenetic trees.
    """

    homepage = "https://github.com/stamatak/ExaML"
    url = "https://github.com/stamatak/ExaML/archive/v3.0.22.tar.gz"

    maintainers("robqiao")

    license("GPL-3.0-only")

    version("3.0.22", sha256="802e673b0c2ea83fdbe6b060048d83f22b6978933a04be64fb9b4334fe318ca3")
    version("3.0.21", sha256="6c7e6c5d7bf4ab5cfbac5cc0d577885272a803c142e06b531693a6a589102e2e")
    version("3.0.20", sha256="023681248bbc7f19821b509948d79301e46bbf275aa90bf12e9f4879639a023b")
    version("3.0.19", sha256="3814230bf7578b8396731dc87ce665d0b1a671d8effd571f924c5b7936ae1c9e")
    version("3.0.18", sha256="1bacb5124d943d921e7beae52b7062626d0ce3cf2f83e3aa3acf6ea26cf9cd87")
    version("3.0.17", sha256="90a859e0b8fff697722352253e748f03c57b78ec5fbc1ae72f7e702d299dac67")
    version("3.0.16", sha256="abc922994332d40892e30f077e4644db08cd59662da8e2a9197d1bd8bcb9aa5f")
    version("3.0.15", sha256="da5e66a63d6fa34b640535c359d8daf67f23bd2fcc958ac604551082567906b0")
    version("3.0.14", sha256="698b538996946ae23a2d6fa1e230c210832e59080da33679ff7d6b342a9e6180")
    version("3.0.13", sha256="893aecb5545798235a17975aa07268693d3526d0aee0ed59a2d6e791248791ed")

    depends_on("c", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI parallel support")

    depends_on("mpi", when="+mpi")

    def build(self, spec, prefix):
        #####################
        # Build Directories #
        #####################
        with working_dir("examl"):
            make("-f", "Makefile.SSE3.gcc")
        with working_dir("parser"):
            make("-f", "Makefile.SSE3.gcc")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("examl/examl", prefix.bin)
        install("parser/parse-examl", prefix.bin)
        install_tree("manual", prefix.manual)
        install_tree("testData", prefix.testData)
