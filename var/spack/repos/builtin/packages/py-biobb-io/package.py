# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiobbIo(PythonPackage):
    """Biobb_io is the Biobb module collection to fetch data to be
    consumed by the rest of the Biobb building blocks"""

    pypi = "biobb_io/biobb_io-4.1.0.tar.gz"

    maintainers("d-beltran")

    # Versions
    version("4.1.0", sha256="074ea97a3682731e13d559b7f91b04e4a3f0f02ee798503089e4af79a730bf72")

    # Dependencies
    depends_on("py-setuptools", type="build")
    depends_on("py-biobb-common@4.1.0", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"))
