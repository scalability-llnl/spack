# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bsseeker2(Package):
    """A versatile aligning pipeline for bisulfite sequencing data."""

    homepage = "http://pellegrini.mcdb.ucla.edu/BS_Seeker2"
    url = "https://github.com/BSSeeker/BSseeker2/archive/BSseeker2-v2.1.8.tar.gz"

    license("MIT")

    version("2.1.8", sha256="34ebedce36a0fca9e22405d4c2c20bc978439d4a34d1d543657fbc53ff847934")
    version(
        "2.1.7",
        sha256="ac90fb4ad8853ee920f1ffea2b1a8cfffcdb1508ff34be0091d5a9c90ac8c74a",
        url="https://github.com/BSSeeker/BSseeker2/archive/v2.1.7.tar.gz",
    )
    version(
        "2.1.2",
        sha256="08055dd314f85a9b74c259c2cb894ea2affdab2c7a120af3589c649e1900c5c6",
        url="https://github.com/BSSeeker/BSseeker2/archive/v2.1.2.tar.gz",
    )

    depends_on("python@2.6:", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("Antisense.py", prefix.bin)
        install_tree("bs_index", prefix.bin.bs_index)
        install("bs_seeker2-build.py", prefix.bin)
        install_tree("bs_utils", prefix.bin.bs_utils)
        install_tree("galaxy", prefix.bin.galaxy)
        install_tree("bs_align", prefix.bin.bs_align)
        install("bs_seeker2-align.py", prefix.bin)
        install("bs_seeker2-call_methylation.py", prefix.bin)
        install("FilterReads.py", prefix.bin)
