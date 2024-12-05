# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xhmm(MakefilePackage):
    """The XHMM C++ software suite was written to
    call copy number variation (CNV) from next-generation
    sequencing projects, where exome capture was used
    (or targeted sequencing, more generally)."""

    homepage = "http://atgu.mgh.harvard.edu/xhmm/index.shtml"
    git = "https://bitbucket.org/statgen/xhmm.git"

    version("20160104", commit="cc14e528d90932f059ac4fe94e869e81221fd732")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("lapack")

    def edit(self, spec, prefix):
        filter_file("GCC", "CC", "sources/hmm++/config_rules.Makefile")
        filter_file("GCC =gcc", "", "sources/hmm++/config_defs.Makefile")

    def build(self, spec, prefix):
        make("LAPACK_LIBS=%s" % "".join(spec["lapack"].libs.names))

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("xhmm", prefix.bin)
