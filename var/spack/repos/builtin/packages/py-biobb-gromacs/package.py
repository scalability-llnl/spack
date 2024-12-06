# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiobbGromacs(PythonPackage):
    """Biobb_gromacs is the Biobb module collection to perform
    molecular dynamics simulations using the GROMACS MD suite"""

    pypi = "biobb_gromacs/biobb_gromacs-4.1.1.tar.gz"

    maintainers("d-beltran")

    # Versions
    version("4.1.1", sha256="270cce747fc214471527438c8319bda0613be5b76da9f4684e6f138d1927d2f7")

    # Dependencies
    depends_on("py-setuptools", type="build")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-biobb-common@4.1.0", type=("build", "run"))
    depends_on("gromacs", type=("run"))
