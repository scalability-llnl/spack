# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAhpy(PythonPackage):
    """AHPy is an implementation of the Analytic Hierarchy Process (AHP), a
    method used to structure, synthesize and evaluate the elements of a
    decision problem."""

    homepage = "https://github.com/PhilipGriffith/AHPy"
    pypi = "ahpy/ahpy-2.0.tar.gz"

    license("MIT")

    version("2.0", sha256="f0af7b81b51466a055778d84f64c98f5cc3e1ba34aaeaedc48ba0b91008e40e3")

    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
