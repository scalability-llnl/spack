# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBreakseq2(PythonPackage):
    """nucleotide-resolution analysis of structural variants"""

    homepage = "https://bioinform.github.io/breakseq2/"
    url = "https://github.com/bioinform/breakseq2/archive/2.2.tar.gz"

    license("BSD-2-Clause")

    version("2.2", sha256="d149e803191e6bb0b749abfba2c258716d94a38e942aaed40eb1630ae84f91ee")

    depends_on("py-setuptools", type="build")
    depends_on("py-biopython@1.65", type=("build", "run"))
    depends_on("py-cython", type="build")
    depends_on("py-pysam@0.7.7", type=("build", "run"))
    depends_on("bwa", type="run")
    depends_on("samtools", type="run")
