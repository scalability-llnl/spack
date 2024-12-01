# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQpth(PythonPackage):
    """A fast and differentiable QP solver for PyTorch"""

    homepage = "https://github.com/locuslab/qpth"
    pypi = "qpth/qpth-0.0.15.tar.gz"

    license("Apache-2.0")

    version("0.0.15", sha256="99d8ec5a35877c18543875a7d5b7fc9af1fa9a4d4b0888011c1ecf42ad9d521c")

    depends_on("python", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1")
    depends_on("py-torch")
    depends_on("py-cvxpy")
