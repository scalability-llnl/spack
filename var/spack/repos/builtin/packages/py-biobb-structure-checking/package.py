# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiobbStructureChecking(PythonPackage):
    """Biobb_structure_checking provides a series of functions
    to check the quality of a 3D structure intended to facilitate
    the setup of a molecular dynamics simulation of protein or nucleic acids systems"""

    pypi = "biobb_structure_checking/biobb_structure_checking-3.14.4.tar.gz"

    maintainers("d-beltran")

    # Versions
    version("3.13.4", sha256="d819819d13c7ad219411b70b043555dcd65d5535f696a1121db562646931f445")

    # Dependencies
    depends_on("py-setuptools", type="build")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-biopython@1.79:", type=("build", "run"))
