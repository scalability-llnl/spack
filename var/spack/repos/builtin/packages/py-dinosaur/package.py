# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDinosaur(PythonPackage):
    """Dinosaur: differentiable dynamics for global atmospheric modeling."""

    homepage = "https://github.com/google-research/dinosaur"
    git = "https://github.com/google-research/dinosaur.git"

    license("Apache-2.0")

    version("main", branch="main")

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:")
        depends_on("py-fsspec")
        depends_on("py-jax")
        depends_on("py-jaxlib")
        depends_on("py-numpy")
        depends_on("py-pandas")
        depends_on("py-pint")
        depends_on("py-scipy")
        depends_on("py-scikit-learn")
        depends_on("py-tree-math")
        depends_on("py-xarray")
        depends_on("py-xarray-tensorstore")
