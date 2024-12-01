# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SoapdenovoTrans(MakefilePackage):
    """SOAPdenovo-Trans is a de novo transcriptome assembler basing on the
    SOAPdenovo framework, adapt to alternative splicing and different
    expression level among transcripts."""

    homepage = "https://github.com/aquaskyline/SOAPdenovo-Trans"
    url = "https://github.com/aquaskyline/SOAPdenovo-Trans/archive/1.0.4.tar.gz"
    maintainers("snehring")

    license("GPL-3.0-only")

    version("1.0.5", sha256="c1903c0d81142270db95916e2833400f72c4841b5c9194f182c19ebda418936f")
    version("1.0.4", sha256="378a54cde0ebe240fb515ba67197c053cf95393645c1ae1399b3a611be2a9795")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api", type="link")
    depends_on("samtools@0.1.8", type="link", when="target=aarch64:")

    build_directory = "src"

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter("Makefile")
            makefile.filter(
                "CFLAGS=         -O3 -fomit-frame-pointer -static",
                "CFLAGS=         -O3 -fomit-frame-pointer",
            )
            if spec.target.family == "aarch64":
                makefile.filter("ppc64 ia64", "ppc64 ia64 aarch64")

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make()
            make("127mer=1", parallel=False)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("SOAPdenovo-Trans-*mer", prefix.bin)
