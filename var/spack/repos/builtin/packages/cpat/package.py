# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cpat(PythonPackage):
    """CPAT is an alignment-free method to predict RNA coding potential using four sequence
    features"""

    homepage = "https://cpat.readthedocs.io/"
    pypi = "CPAT/CPAT-3.0.4.tar.gz"

    version("3.0.4", sha256="6d832f20729f8fc814384a27a4fcebcf81b11c0e6d80a404b4c4860d17e7d935")

    depends_on("py-setuptools", type="build")
    depends_on("py-nose@0.10.4:", type="build")
    depends_on("py-cython@0.17:", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))

    depends_on("r", type="run")
