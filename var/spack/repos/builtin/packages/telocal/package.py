# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Telocal(PythonPackage):
    """A package for quantifying transposable elements at a locus level for RNAseq datasets"""

    homepage = "https://hammelllab.labsites.cshl.edu/software/#TElocal"

    url = "https://github.com/mhammell-laboratory/TElocal/archive/refs/tags/1.1.2.tar.gz"

    license("GPL-3.0-only", checked_by="A_N_Other")

    version("1.1.2", sha256="d0c7d419d7df06dedbdffbf316fe01fa7324994e0fe1c4ea721835ec9b3e9bb5")

    depends_on("py-setuptools", type="build")
    depends_on("py-pysam@0.9:", type=("build", "run"))
