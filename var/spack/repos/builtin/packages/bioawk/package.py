# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bioawk(MakefilePackage):
    """Bioawk is an extension to Brian Kernighan's awk, adding the support of
    several common biological data formats, including optionally gzip'ed
    BED, GFF, SAM, VCF, FASTA/Q and TAB-delimited formats with column names.
    """

    homepage = "https://github.com/lh3/bioawk"
    url = "https://github.com/lh3/bioawk/archive/v1.0.zip"

    version("1.0", sha256="316a6561dda41e8327b85106db3704e94e23d7a89870392d19ef8559f7859e2d")

    depends_on("zlib-api")
    depends_on("bison", type=("build"))

    parallel = False

    def build(self, spec, prefix):
        make("CC={0}".format(spack_cc))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("bioawk", prefix.bin)
        install("maketab", prefix.bin)
