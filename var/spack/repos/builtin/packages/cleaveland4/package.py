# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cleaveland4(Package):
    """CleaveLand4: Analysis of degradome data to find sliced miRNA and siRNA
    targets"""

    homepage = "https://github.com/MikeAxtell/CleaveLand4"
    url = "https://github.com/MikeAxtell/CleaveLand4/archive/v4.4.tar.gz"

    license("GPL-3.0-or-later")

    version("4.5", sha256="d0ad584a8bc2391cdee5f6279b2351f7db972362669467564e6bd3f94dcd9dd1")
    version("4.4", sha256="bf7fe6ad730ea2bfb2e0c0f863734f189073a69b1754532012f1261b368b24e7")

    depends_on("perl", type=("build", "run"))
    depends_on("perl-math-cdf", type=("build", "run"))
    depends_on("bowtie")
    depends_on("viennarna")
    depends_on("r", type=("build", "run"))
    depends_on("samtools")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("CleaveLand4.pl", prefix.bin)
        with working_dir("GSTAr_v1-0"):
            install("GSTAr.pl", prefix.bin)
