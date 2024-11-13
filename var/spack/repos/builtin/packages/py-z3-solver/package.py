# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZ3Solver(PythonPackage):
    """Z3 is a theorem prover from Microsoft Research. It is licensed under the MIT license."""

    homepage = "https://github.com/Z3Prover/z3"
    pypi = "z3-solver/z3-solver-4.12.3.0.tar.gz"

    license("MIT")

    version("4.12.3.0", sha256="b6719daf9676711a8f1c708af0ea185578b0f22a3cb9bf9a55735e21691dc38d")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools@46.4:", type="build")
    depends_on("cmake", type="build")
