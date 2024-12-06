# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bucky(MakefilePackage):
    """BUCKy is a free program to combine molecular data from multiple loci.
    BUCKy estimates the dominant history of sampled individuals, and how
    much of the genome supports each relationship, using Bayesian
    concordance analysis."""

    homepage = "https://www.stat.wisc.edu/~ane/bucky/index.html"
    url = "http://dstats.net/download/http://www.stat.wisc.edu/~ane/bucky/v1.4/bucky-1.4.4.tgz"
    maintainers("snehring")

    version("1.4.4", sha256="1621fee0d42314d9aa45d0082b358d4531e7d1d1a0089c807c1b21fbdc4e4592")

    requires("%gcc", msg="bucky can only be compiled with GCC")

    build_directory = "src"

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            filter_file("g++", spack_cxx, "makefile", string=True)

    def install(self, spec, prefix):
        with working_dir("src"):
            mkdirp(prefix.bin)
            install("bucky", prefix.bin)
            install("mbsum", prefix.bin)
        install_tree("data", prefix.data)
        install_tree("doc", prefix.doc)
        install_tree("scripts", prefix.scripts)

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%gcc@5:") and name.lower() == "cxxflags":
            flags.append(self.compiler.cxx98_flag)
        return (flags, None, None)
