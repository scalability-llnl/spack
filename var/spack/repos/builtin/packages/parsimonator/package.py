# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Parsimonator(MakefilePackage):
    """Parsimonator is a no-frills light-weight implementation for building
    starting trees under parsimony for RAxML.
    """

    homepage = "http://www.exelixis-lab.org/"
    git = "https://github.com/stamatak/Parsimonator-1.0.2.git"

    version("1.0.2", commit="78368c6ab1e9adc7e9c6ec9256dd7ff2a5bb1b0a")

    depends_on("c", type="build")  # generated

    patch("nox86.patch")

    @property
    def makefile_file(self):
        if self.spec.target.family != "x86_64":
            return "Makefile.nosse"

        if "avx" in self.spec.target:
            return "Makefile.AVX.gcc"
        elif "sse3" in self.spec.target:
            return "Makefile.SSE3.gcc"

        return "Makefile.gcc"

    def edit(self, spec, prefix):
        makefile = FileFilter(self.makefile_file)
        makefile.filter("CC = gcc", "CC = %s" % spack_cc)

    def build(self, spec, prefix):
        make("-f", self.makefile_file)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if "avx" in self.spec.target:
            install("parsimonator-AVX", prefix.bin)
        elif "sse3" in self.spec.target:
            install("parsimonator-SSE3", prefix.bin)
        else:
            install("parsimonator", prefix.bin)
