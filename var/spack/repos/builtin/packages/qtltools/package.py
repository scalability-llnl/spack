# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qtltools(MakefilePackage):
    """A complete tool set for molecular QTL discovery and analysis."""

    homepage = "https://qtltools.github.io/qtltools/"
    url = "https://github.com/qtltools/qtltools/archive/refs/tags/1.3.1.tar.gz"

    license("GPL-3.0-only")

    version("1.3.1", sha256="033b9b61923fd65c4b8b80bc0add321e6fd6fb40de49d15c2dfe6a4d7e60764a")
    version("1.3", sha256="032020d7e038eac4ec01701343a887bced7cca356cbd24b3d5bbadf83686faeb")

    depends_on("cxx", type="build")  # generated

    depends_on("boost +pic +iostreams +program_options")
    depends_on("gsl")
    depends_on("htslib ~libcurl ~libdeflate")
    depends_on("r +rmath")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("BOOST_INC=.*", "BOOST_INC=" + self.spec["boost"].prefix.include)
        makefile.filter("BOOST_LIB=.*", "BOOST_LIB=" + self.spec["boost"].prefix.lib)
        makefile.filter("RMATH_INC=.*", "RMATH_INC=" + self.spec["r"].prefix.include)
        makefile.filter("RMATH_LIB=.*", "RMATH_LIB=" + self.spec["r"].prefix.rlib)
        makefile.filter("HTSLD_INC=.*", "HTSLD_INC=" + self.spec["htslib"].prefix.include)
        makefile.filter("HTSLD_LIB=.*", "HTSLD_LIB=" + self.spec["htslib"].prefix.lib)
        makefile.filter("prefix *=.*", "prefix = " + prefix)
