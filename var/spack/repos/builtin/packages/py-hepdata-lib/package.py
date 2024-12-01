# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHepdataLib(PythonPackage):
    """Library for getting your data into HEPData"""

    homepage = "https://github.com/HEPData/hepdata_lib"
    # PyPI archives are broken: missing requirement.txt file
    # pypi = "hepdata_lib/hepdata_lib-0.9.0.tar.gz"
    url = "https://github.com/HEPData/hepdata_lib/archive/refs/tags/v0.9.0.tar.gz"

    license("MIT")

    version("0.10.1", sha256="71c635963883c51e7be18e03d80bfe42c5de350852b01010e3e45cbd1bff7a81")
    version("0.9.0", sha256="c9238e45c603d7c061ed670cf197ff03ad9d370ab50419b6916fda2cd86d6150")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("root+python", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pyyaml@5:", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-pytest-runner", type="build")
    depends_on("py-pytest-cov", type="build")
    depends_on("py-hepdata-validator@0.3.2:", when="@0.10.1:", type=("build", "run"))
