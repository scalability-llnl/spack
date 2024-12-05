# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMedaka(PythonPackage):
    """medaka is a tool to create consensus sequences and variant calls from
    nanopore sequencing data. This task is performed using neural networks
    applied a pileup of individual sequencing reads against a draft assembly.
    It provides state-of-the-art results outperforming sequence-graph based
    methods and signal-based methods, whilst also being faster."""

    homepage = "https://github.com/nanoporetech/medaka"
    pypi = "medaka/medaka-1.7.2.tar.gz"

    license("MPL-2.0")

    version("1.7.2", sha256="7629546ed9193ffb6b1f881a6ce74b7d13d94972e032556098577ddb43bee763")

    # disable Makefile driven build of htslib and link to system htslib instead
    patch("htslib.patch", when="@1.7.2")

    depends_on("python@3.6:3.9", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cffi@1.15.0", type=("build", "run"))
    depends_on("py-edlib", type=("build", "run"))
    depends_on("py-grpcio", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-intervaltree", type=("build", "run"))
    depends_on("py-tensorflow@2.7.0:2.7", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("minimap2", type=("build", "run"))
    depends_on("py-ont-fast5-api", type=("build", "run"))
    depends_on("py-parasail", when="target=x86_64:", type=("build", "run"))
    depends_on("py-parasail", when="target=ppc64le:", type=("build", "run"))
    depends_on("py-pysam@0.16.0.1:", type=("build", "run"))
    depends_on("py-pyspoa@0.0.3:", when="target=x86_64:", type=("build", "run"))
    depends_on("py-pyspoa@0.0.3:", when="target=ppc64le:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("samtools", type=("build", "run"))
    depends_on("htslib", type=("build", "run", "link"))
