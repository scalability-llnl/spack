# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpherical(PythonPackage):
    """Evaluate and transform D matrices, 3-j symbols, and (scalar or
    spin-weighted) spherical harmonics"""

    homepage = "https://github.com/moble/spherical"
    pypi = "spherical/spherical-1.0.10.tar.gz"

    maintainers("nilsvu", "moble")

    license("MIT")

    version("1.0.10", sha256="a7f1d902aa89fd51174a0c69b2379c352d229bf7e088907e8eb4461ad227d95f")

    depends_on("python@3.6:3.9", type=("build", "run"))
    depends_on("py-poetry-core@1.0.1:", type="build")
    depends_on("py-importlib-metadata@1:", when="^python@:3.7", type=("build", "run"))
    depends_on("py-numpy@1.13:", type=("build", "run"))
    depends_on("py-numba@0.50:", type=("build", "run"))
    depends_on("py-quaternionic@1:", type=("build", "run"))
