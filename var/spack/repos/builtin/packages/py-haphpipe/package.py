# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHaphpipe(PythonPackage):
    """HAplotype and PHylodynamics pipeline for viral assembly,
    population genetics, and phylodynamics."""

    homepage = "https://github.com/gwcbi/haphpipe"
    url = "https://github.com/gwcbi/haphpipe/archive/v1.0.3.tar.gz"

    maintainers("dorton21")

    license("GPL-3.0-or-later")

    version("1.0.3", sha256="9a9e8632a217ff4207c1dea66887a471e0ea04bbb7c0f0d72631acaba214bd37")

    # Deps. taken from
    # https://github.com/bioconda/bioconda-recipes/blob/master/recipes/haphpipe/meta.yaml
    # https://bioconda.github.io/recipes/haphpipe/README.html
    # https://github.com/gwcbi/haphpipe/blob/master/environment.yml
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-biopython@1.73:", type=("build", "run"))
    depends_on("py-gsutil", type=("build", "run"))
    depends_on("py-sierrapy", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("bowtie2", type=("build", "run"))
    depends_on("blast-plus", type=("build", "run"))
    depends_on("freebayes", type=("build", "run"))
    depends_on("modeltest-ng", type=("build", "run"))
    depends_on("libdeflate", type=("build", "run"))
    depends_on("sratoolkit", type=("build", "run"))
    depends_on("spades", type=("build", "run"))
    depends_on("seqtk", type=("build", "run"))
    depends_on("raxml-ng~mpi", type=("build", "run"))
    depends_on("gatk@3.8-0", type=("build", "run"))
    depends_on("trinity", type=("build", "run"))
    depends_on("trimmomatic@0.38:", type=("build", "run"))
    depends_on("flash@1.2.11:", type=("build", "run"))
    depends_on("mummer@3.23:", type=("build", "run"))
    depends_on("bwa", type=("build", "run"))
    depends_on("samtools@1.9:", type=("build", "run"))
    depends_on("mafft", type=("build", "run"))
    depends_on("picard", type=("build", "run"))
