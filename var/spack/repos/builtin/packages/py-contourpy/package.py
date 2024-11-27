# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyContourpy(PythonPackage):
    """Python library for calculating contours of 2D quadrilateral grids."""

    homepage = "https://github.com/contourpy/contourpy"
    pypi = "contourpy/contourpy-1.0.5.tar.gz"

    license("BSD-3-Clause")

    version("1.3.0", sha256="7ffa0db17717a8ffb127efd0c95a4362d996b892c2904db72428d5b52e1938a4")
    version("1.0.7", sha256="d8165a088d31798b59e91117d1f5fc3df8168d8b48c4acc10fc0df0d0bdbcc5e")
    version("1.0.5", sha256="896631cd40222aef3697e4e51177d14c3709fda49d30983269d584f034acc8a4")

    depends_on("py-pybind11", type=("build", "link"))
    depends_on("cxx", type="build")

    with default_args(type="build"):
        depends_on("meson@1.2:")
        depends_on("py-meson-python@0.13.1:")
        with default_args(type=("build", "link")):
            depends_on("py-pybind11@2.13.1:", when="@1.3:")
            depends_on("py-pybind11@2.6:")

        # Historical dependencies
        depends_on("py-setuptools@42:", when="@:1.0")
        depends_on("py-build", when="@:1.0.5")

    with default_args(type=("build", "link", "run")):
        depends_on("python@3.9:", when="@1.3:")
        depends_on("python@3.8:", when="@1.0.7:")
        depends_on("python@3.7:")

    with default_args(type=("build", "run")):
        depends_on("py-numpy@1.23:", when="@1.3:")
        depends_on("py-numpy@1.16:")

    # https://github.com/numpy/numpy/issues/26191
    conflicts("py-numpy@2:", when="@:1.2.0")
    conflicts("py-pybind11@2.13.3")
