# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiomine(PythonPackage):
    """Bioinformatics data-mining."""

    homepage = "https://github.com/AdamDS/BioMine"
    url = "https://github.com/AdamDS/BioMine/archive/v0.9.5.tar.gz"

    license("MIT")

    version("0.9.5", sha256="1b2a72cd2cb6e99d9b79fcc9ea94fa0e1892b02465620ba6bba59473dc7ff3ac")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-advancedhtmlparser", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))
    depends_on("py-pyvcf", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
