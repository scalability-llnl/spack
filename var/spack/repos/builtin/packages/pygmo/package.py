# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pygmo(CMakePackage):
    """Parallel Global Multiobjective Optimizer (and its Python alter ego
    PyGMO) is a C++ / Python platform to perform parallel computations of
    optimisation tasks (global and local) via the asynchronous generalized
    island model."""

    homepage = "https://esa.github.io/pygmo2/"
    url = "https://github.com/esa/pygmo2/archive/v2.18.0.tar.gz"
    git = "https://github.com/esa/pygmo2.git"

    license("MPL-2.0")

    version("master", branch="master")
    version("2.18.0", sha256="9f081cc973297894af09f713f889870ac452bfb32b471f9f7ba08a5e0bb9a125")

    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")

    # Run-time dependencies
    # https://github.com/esa/pygmo2/blob/master/doc/install.rst#dependencies
    extends("python@3.4:")
    depends_on("pagmo2@2.18:")
    depends_on("boost@1.60:")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-cloudpickle", type=("build", "run"))

    # Build-time dependencies
    # https://github.com/esa/pygmo2/blob/master/doc/install.rst#installation-from-source
    depends_on("py-pybind11@2.6:", type="build")
    depends_on("cmake@3.17:", type="build")

    def cmake_args(self):
        return [
            self.define("PYGMO_INSTALL_PATH", python_platlib),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]
