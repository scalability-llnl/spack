# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQuaternionic(PythonPackage):
    """Interpret numpy arrays as quaternionic arrays with numba acceleration"""

    homepage = "https://github.com/moble/quaternionic"
    pypi = "quaternionic/quaternionic-1.0.1.tar.gz"

    maintainers("nilsvu", "moble")

    license("MIT")

    version("1.0.1", sha256="ea69733d7311784963922bf08cc0c9c938b62fee2f91219f56544ff30658c10e")

    depends_on("python@3.6:3.9", type=("build", "run"))
    depends_on("py-poetry-core@1.0.1:", type="build")
    depends_on("py-importlib-metadata@1:", when="^python@:3.7", type=("build", "run"))
    depends_on("py-numpy@1.13:", type=("build", "run"))
    depends_on("py-scipy@1:", type=("build", "run"))
    depends_on("py-numba@0.50:", type=("build", "run"))
