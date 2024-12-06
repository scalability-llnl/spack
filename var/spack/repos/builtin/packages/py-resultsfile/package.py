# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyResultsfile(PythonPackage):
    """Python module to read output files of quantum chemistry programs"""

    homepage = "https://gitlab.com/scemama/resultsFile"
    url = "https://gitlab.com/scemama/resultsFile/-/archive/v1.0/resultsFile-v1.0.tar.gz"
    git = "https://gitlab.com/scemama/resultsFile.git"

    maintainers("scemama")

    license("GPL-2.0-only")

    version("2.0", sha256="2a34208254e4bea155695690437f6a59bf5f7b0ddb421d6c1a2d377510f018f7")

    depends_on("python@3:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
