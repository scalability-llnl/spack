# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tetranscripts(PythonPackage):
    """TEtranscripts: Tools for estimating differential enrichment of Transposable Elements
    and other highly repetitive regions."""

    homepage = "https://hammelllab.labsites.cshl.edu/software/#TEtranscripts"
    pypi = "TEtranscripts/TEtranscripts-2.2.3.tar.gz"

    license("GPL-3.0-only")

    version("2.2.3", sha256="e53577e8e73e41c6495fb819977e3e537bbeac7b2fa1635029201a37ee0bf7b8")

    # python dependencies
    depends_on("py-setuptools", type="build")
    depends_on("py-pysam@0.9:", type=("build", "run"))
    # external dependencies
    depends_on("r@2.15:", type="run")
    depends_on("r-deseq2@1.10:", type="run")
