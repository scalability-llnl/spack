# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVcfKit(PythonPackage):
    """VCF-kit is a command-line based collection of utilities for performing
    analysis on Variant Call Format (VCF) files."""

    homepage = "https://github.com/AndersenLab/VCF-kit"
    url = "https://github.com/AndersenLab/VCF-kit/archive/0.1.6.tar.gz"

    license("MIT")

    version("0.1.6", sha256="4865414ac9dc6996c0baeefadf1d528c28e6d0c3cc3dbdc28a2cdc6e06212428")

    depends_on("python", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-awesome-slugify", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-cython@0.24.1:", type="build")
    depends_on("py-cyvcf2@0.6.5:", type=("build", "run"))
    depends_on("py-docopt", type=("build", "run"))
    depends_on("py-biopython", type=("build", "run"))
    depends_on("py-yahmm@1.1.2", type=("build", "run"))
    depends_on("py-clint", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-networkx@1.11", type=("build", "run"))
    depends_on("py-intervaltree@2.1.0", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))

    depends_on("bwa@0.7.12:", type="run")
    depends_on("samtools@1.3:", type="run")
    depends_on("bcftools@1.3:", type="run")
    depends_on("blast-plus@2.2.31:", type="run")
    depends_on("muscle@3.8.31:", type="run")
    depends_on("primer3", type="run")
    depends_on("vcftools", type="run")
