# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCylp(PythonPackage):
    """A Python interface for CLP, CBC, and CGL.

    CyLP is a Python interface to COIN-OR's Linear and mixed-integer program
    solvers (CLP, CBC, and CGL). CyLP's unique feature is that you can use it
    to alter the solution process of the solvers from within Python.
    """

    homepage = "https://github.com/coin-or/cylp"
    pypi = "cylp/cylp-0.91.5.tar.gz"

    license("EPL-2.0")

    version("0.91.5", sha256="d68ab1dde125be60abf45c8fd9edd24ab880c8144ad881718ddfa01ff6674c77")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-cython@:2", type="build")

    depends_on("py-numpy@1.5:", type=("build", "run"))
    depends_on("py-scipy@0.10.0:", type=("build", "run"))

    depends_on("cbc")
