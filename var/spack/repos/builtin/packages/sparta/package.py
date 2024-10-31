# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sparta(Package):
    """small RNA-PARE Target Analyzer (sPARTA) is a tool which utilizes
    high-throughput sequencing to profile genome-wide cleavage
    products."""

    homepage = "https://github.com/atulkakrana/sPARTA.github"
    url = "https://github.com/atulkakrana/sPARTA/archive/1.25.tar.gz"

    version("1.27", sha256="6f66a646bd4ecf14fc4dc1e5729e44a740c205b5f0e0f7771ae22f14b047931e")
    version("1.25", sha256="007997b9bf5041ae35c9bb79455d533c0f0773f9dd3ba4e5ddf306139625681f")

    depends_on("bowtie2")
    depends_on("python@3:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("sPARTA.py", prefix.bin)
        install("revFernoMap.py", prefix.bin)
