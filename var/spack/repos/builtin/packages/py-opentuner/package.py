# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpentuner(PythonPackage):
    """An extensible framework for program autotuning."""

    homepage = "https://opentuner.org/"
    git = "https://github.com/jansel/opentuner.git"

    maintainers("matthiasdiener")

    license("MIT")

    version("0.8.7", commit="070c5cef6d933eb760a2f9cd5cd08c95f27aee75")
    version("0.8.2", commit="8e720a2094e7964d7a1225e58aca40b0e78bff7d")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3:", type=("build", "run"), when="@0.8.1:")

    depends_on("py-fn-py@0.2.12:", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-numpy@1.8.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-sqlalchemy@0.8.2:", type=("build", "run"))
