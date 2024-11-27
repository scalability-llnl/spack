# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPauvre(PythonPackage):
    """pauvre: plotting package designed for nanopore and PacBio long reads"""

    homepage = "https://github.com/conchoecia/pauvre"
    url = "https://github.com/conchoecia/pauvre/archive/0.1.86.tar.gz"

    version("0.1.86", sha256="aa0b3653e7c12fb50a0907ce088d85b8e1b52c97f40e4d2e6e6b7525a681aa1a")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-biopython", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
