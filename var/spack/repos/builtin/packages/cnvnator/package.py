# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cnvnator(MakefilePackage):
    """A tool for CNV discovery and genotyping
    from depth-of-coverage by mapped reads."""

    homepage = "https://github.com/abyzovlab/CNVnator"
    url = "https://github.com/abyzovlab/CNVnator/archive/v0.3.3.tar.gz"

    version("0.3.3", sha256="58c5acf61f9a1e5febf546c196f8917a5e084b729e5c4cfd3eba83471b3fe5c1")

    depends_on("cxx", type="build")  # generated

    depends_on("samtools@:1.13")
    depends_on("htslib")
    depends_on("root")
    depends_on("bzip2")
    depends_on("curl")
    depends_on("xz")
    depends_on("zlib-api")
    depends_on("libdeflate")
    depends_on("openssl")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        # Replace -fopenmp with self.compiler.openmp_flag
        makefile.filter("-fopenmp", self.compiler.openmp_flag)
        # Replace CXX with CXXFLAGS
        makefile.filter(
            "CXX.*=.*",
            r"CXXFLAGS = -DCNVNATOR_VERSION=\"$(VERSION)\""
            " $(OMPFLAGS)"
            " {0}".format(self.compiler.cxx11_flag),
        )
        makefile.filter("$(CXX)", "$(CXX) $(CXXFLAGS)", string=True)
        # Replace -I$(SAMDIR) with -I$(SAMINC)
        makefile.filter("-I$(SAMDIR)", "-I$(SAMINC)", string=True)

        # Link more libs
        ldflags = [
            spec["zlib-api"].libs.ld_flags,
            spec["bzip2"].libs.ld_flags,
            spec["curl"].libs.ld_flags,
            spec["xz"].libs.ld_flags,
            spec["libdeflate"].libs.ld_flags,
            spec["openssl"].libs.ld_flags,
        ]
        makefile.filter("^override LIBS.*", "override LIBS += {0}".format(" ".join(ldflags)))

    def build(self, spec, prefix):
        make(
            "ROOTSYS={0}".format(spec["root"].prefix),
            "SAMINC={0}".format(spec["samtools"].prefix.include),
            "SAMDIR={0}".format(spec["samtools"].prefix.lib),
            "HTSDIR={0}".format(spec["htslib"].prefix.lib),
        )

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("cnvnator", prefix.bin)
