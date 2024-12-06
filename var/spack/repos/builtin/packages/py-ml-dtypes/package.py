# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMlDtypes(PythonPackage):
    """A stand-alone implementation of several NumPy dtype extensions
    used in machine learning libraries."""

    homepage = "https://github.com/jax-ml/ml_dtypes"
    pypi = "ml_dtypes/ml_dtypes-0.3.1.tar.gz"
    git = "https://github.com/jax-ml/ml_dtypes.git"
    submodules = True

    license("Apache-2.0")

    version("0.4.0", tag="v0.4.0", commit="9fc7e6773acb66fa496ed8d476a008a489a4da49")
    version("0.3.1", tag="v0.3.1", commit="bbeedd470ecac727c42e97648c0f27bfc312af30")
    version("0.2.0", tag="v0.2.0", commit="5b9fc9ad978757654843f4a8d899715dbea30e88")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("python@3.9:", when="@0.3:", type=("build", "link", "run"))
    depends_on("py-numpy@1.21:", type=("build", "link", "run"))
    # https://github.com/jax-ml/ml_dtypes/pull/143
    depends_on("py-numpy@:1", when="@:0.3", type=("build", "link", "run"))
    # Build dependencies are overconstrained, older versions work just fine
    depends_on("py-pybind11", when="@:0.3.1", type=("build", "link"))
    depends_on("py-setuptools", type="build")
