# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUnicycler(PythonPackage):
    """Unicycler is an assembly pipeline for bacterial genomes. It can
    assemble Illumina-only read sets where it functions as a SPAdes-optimiser.
    It can also assembly long-read-only sets (PacBio or Nanopore) where it
    runs a miniasm+Racon pipeline. For the best possible assemblies, give it
    both Illumina reads and long reads, and it will conduct a hybrid assembly.
    """

    homepage = "https://github.com/rrwick/Unicycler"
    url = "https://github.com/rrwick/Unicycler/archive/v0.4.5.tar.gz"

    license("GPL-3.0-or-later")

    version("0.5.0", sha256="84a8709c9f2e624225410af702d779ffb0cb06f7c22c20e1f01b989945e08a47")
    version("0.4.9", sha256="84bea8f3e8f99a1e63e5230ffe474a696db8caa67569c3a96ae12906d32a35eb")
    version("0.4.8", sha256="e948871e4de9db5964c9ca6f8f877c3cbe6a46f62052dfab52ffe0f45bbbd203")
    version("0.4.7", sha256="a8cf65e46dc2694b0fbd4e9190c73a1f300921457aadfab27a1792b785620d63")
    version("0.4.6", sha256="56f6f358a5d1f8dd0fcd1df04504079fc42cec8453a36ee59ff89295535d03f5")
    version("0.4.5", sha256="67043656b31a4809f8fa8f73368580ba7658c8440b9f6d042c7f70b5eb6b19ae")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.4:", type=("build", "link", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("racon", type=("build", "link", "run"))
    depends_on("blast-plus", type="run")

    # for version 0.5.0
    depends_on("spades@3.14.0:", type="run", when="@0.5.0")

    # for versions 0.4.9 and earlier
    depends_on("spades@3.6.2:3.13.0", type="run", when="@:0.4.9")
    depends_on("pilon", type="run", when="@:0.4.9")
    depends_on("java", type=("build", "run"), when="@:0.4.9")
    depends_on("bowtie2", type="run", when="@:0.4.9")
    depends_on("samtools@1.0:", type=("build", "link", "run"), when="@:0.4.9")

    conflicts("%gcc@:4.9.0")
    conflicts("%clang@:3.4.2")
