# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gffread(MakefilePackage):
    """gffread: GFF/GTF utility providing format conversions, region filtering,
    FASTA sequence extraction and more"""

    homepage = "https://ccb.jhu.edu/software/stringtie/gff.shtml#gffread"
    url = "https://github.com/gpertea/gffread/releases/download/v0.12.7/gffread-0.12.7.tar.gz"

    license("MIT")

    version("0.12.7", sha256="bfde1c857495e578f5b3af3c007a9aa40593e69450eafcc6a42c3e8ef08ed1f5")

    depends_on("cxx", type="build")  # generated

    def build(self, spec, prefix):
        make("release")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("gffread", prefix.bin)
