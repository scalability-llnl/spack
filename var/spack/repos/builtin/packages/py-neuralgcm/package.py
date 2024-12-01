# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeuralgcm(PythonPackage):
    """NeuralGCM: Hybrid ML + Physics model of Earth's atmosphere."""

    homepage = "https://github.com/google-research/neuralgcm"
    git = "https://github.com/google-research/neuralgcm.git"

    license("Apache-2.0")

    version("main", branch="main")

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:")
        depends_on("py-dinosaur")
        depends_on("py-dm-haiku")
        depends_on("py-gin-config")
        depends_on("py-jax")
        depends_on("py-jaxlib")
        depends_on("py-numpy")
        depends_on("py-optax")
        depends_on("py-pandas")
        depends_on("py-tensorflow-probability")
        depends_on("py-xarray")
