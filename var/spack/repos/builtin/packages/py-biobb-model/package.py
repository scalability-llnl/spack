# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiobbModel(PythonPackage):
    """Biobb_model is the Biobb module collection to check and model 3d structures,
    create mutations or reconstruct missing atoms"""

    pypi = "biobb_model/biobb_model-4.1.0.tar.gz"

    maintainers("d-beltran")

    # Versions
    version("4.1.0", sha256="616898c26c8196fcf109c97fc03103d1cf5c9cf3eda22bdef5420393cc1906c6")

    # Dependencies
    depends_on("py-setuptools", type="build")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-biobb-common@4.1.0", type=("build", "run"))
    depends_on("py-biobb-structure-checking@3.13.4:", type=("build", "run"))
    depends_on("py-xmltodict", type=("build", "run"))
