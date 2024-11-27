# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Demuxlet(AutotoolsPackage):
    """Genetic multiplexing of barcoded single cell RNA-seq"""

    homepage = "https://github.com/statgen/demuxlet"
    url = "https://github.com/statgen/demuxlet"
    git = "https://github.com/statgen/demuxlet.git"

    maintainers("snehring")

    license("Apache-2.0")

    version("20210211", commit="f5044eb9ed5c6678aa3a80a8f2be7db7748ee732")

    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("htslib@1.10")
    depends_on("libdeflate", when="^htslib+libdeflate")

    def patch(self):
        filter_file("-I ../../htslib/htslib", "", "Makefile.am", string=True)
        filter_file("-I ../htslib/", "", "Makefile.am", string=True)
        filter_file("../htslib/libhts.a", "-lhts", "Makefile.am", string=True)
        if self.spec.satisfies("^htslib+libdeflate"):
            filter_file("-lcrypto", "-lcrypto -ldeflate", "Makefile.am", string=True)

    def autoreconf(self, spec, prefix):
        which("autoreconf")("-vfi")
