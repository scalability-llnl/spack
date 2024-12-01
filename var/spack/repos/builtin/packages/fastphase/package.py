# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastphase(Package):
    """Software for haplotype reconstruction, and estimating missing genotypes
    from population data."""

    homepage = "https://stephenslab.uchicago.edu/software.html"
    url = "http://scheet.org/code/Linuxfp.tar.gz"

    version(
        "2016-03-30", sha256="f0762eaae38b276bccb567d1519fa19bf35fd4078e57cbf13c7d7054150c4f36"
    )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("fastPHASE", prefix.bin)
