# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shapeit4(MakefilePackage):
    """SHAPEIT4 is a fast and accurate method for estimation of haplotypes
    (aka phasing) for SNP array and high coverage sequencing data."""

    homepage = "https://odelaneau.github.io/shapeit4/"
    url = "https://github.com/odelaneau/shapeit4/archive/v4.1.3.tar.gz"

    license("MIT")

    version("4.2.2", sha256="9f109e307b5cc22ab68e7bf77de2429a9bbb2212d66303386e6a3dd81a5bc556")
    version("4.1.3", sha256="d209731277b00bca1e3478b7e0a0cbe40fbe23826c3d640ad12e0dd6033cbbb8")

    depends_on("cxx", type="build")  # generated

    maintainers("ilbiondo")

    depends_on("htslib")
    depends_on("boost+exception+container+iostreams+program_options")
    depends_on("bzip2")
    depends_on("xz")

    def edit(self, spec, prefix):
        makefile = FileFilter("makefile")
        makefile.filter("CXX=.*", "CXX = c++")

        makefile.filter("CXXFLAG=.*", "CXXFLAG = -O3")
        makefile.filter("LDFLAG=.*", "LDFLAG = -O3")

        makefile.filter("HTSLIB_INC=.*", "HTSLIB_INC = " + self.spec["htslib"].prefix.include)

        makefile.filter(
            "HTSLIB_LIB=.*", "HTSLIB_LIB = " + self.spec["htslib"].prefix.lib + "/libhts.so"
        )

        makefile.filter("BOOST_INC=.*", "BOOST_INC = " + self.spec["boost"].prefix.include)

        makefile.filter(
            "BOOST_LIB_IO=.*",
            "BOOST_LIB_IO = " + self.spec["boost"].prefix.lib + "/libboost_iostreams.so",
        )

        makefile.filter(
            "BOOST_LIB_PO=.*",
            "BOOST_LIB_PO = " + self.spec["boost"].prefix.lib + "/libboost_program_options.so",
        )

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("test", join_path(self.prefix, "test"))
        install_tree("docs", join_path(self.prefix, "docs"))
        install_tree("maps", join_path(self.prefix, "maps"))
