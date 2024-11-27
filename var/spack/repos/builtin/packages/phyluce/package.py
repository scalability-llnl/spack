# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Phyluce(PythonPackage):
    """phyluce (phy-loo-chee) is a software package that was initially
    developed for analyzing data collected from ultraconserved
    elements in organismal genomes"""

    homepage = "https://github.com/faircloth-lab/phyluce"
    url = "https://github.com/faircloth-lab/phyluce/archive/v1.6.7.tar.gz"

    license("BSD-3-Clause")

    version("1.6.7", sha256="98c213ab1610506722ad1440ffc93f9cbc78d8b3aaf3d9a47837e1231452cdb6")

    extends("python")
    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-biopython", type="run")

    # runtime binary dependencies
    depends_on("abyss", type="run")
    depends_on("bcftools", type="run")
    depends_on("bwa", type="run")
    depends_on("gatk", type="run")
    depends_on("gblocks", type="run")
    depends_on("lastz", type="run")
    depends_on("mafft", type="run")
    depends_on("muscle", type="run")
    depends_on("picard", type="run")
    depends_on("raxml+pthreads", type="run")
    depends_on("samtools", type="run")
    depends_on("seqtk", type="run")
    depends_on("spades", type="run")
    depends_on("trimal", type="run")
    depends_on("trinity", type="run")
    depends_on("velvet", type="run")
