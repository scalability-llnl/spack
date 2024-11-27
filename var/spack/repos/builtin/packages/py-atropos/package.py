# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAtropos(PythonPackage):
    """Atropos is tool for specific, sensitive, and speedy trimming of NGS
    reads. It is a fork of the venerable Cutadapt read trimmer."""

    homepage = "https://atropos.readthedocs.io"
    pypi = "atropos/atropos-1.1.22.tar.gz"
    git = "https://github.com/jdidion/atropos.git"

    license("MIT")

    version("1.1.22", sha256="05e40cb9337421479c692e1154b962fbf811d7939b72c197a024929b7ae88b78")

    depends_on("c", type="build")  # generated

    depends_on("python@3.3:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-cython@0.25.2:", type="build")
    depends_on("py-tqdm", type=("build", "run"), when="+tqdm")
    depends_on("py-pysam", type=("build", "run"), when="+pysam")

    variant("tqdm", default=False, description="Enable progress bar")
    variant("pysam", default=False, description="Enable bam file parsing")
