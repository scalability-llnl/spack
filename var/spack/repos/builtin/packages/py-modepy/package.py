# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyModepy(PythonPackage):
    """Basis Functions and Node Sets for Interpolation"""

    homepage = "http://documen.tician.de/modepy"
    pypi = "modepy/modepy-2021.1.tar.gz"
    git = "https://github.com/inducer/modepy.git"

    maintainers("cgcgcg")

    license("MIT")

    version("2021.1", sha256="4cddd2d4720128356e0019e8d972d979552eafad059f4acef01e106b22d8d297")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pytools@2013.1:", type=("build", "run"))
    depends_on("py-pytest@2.3:", type=("build", "run"))
