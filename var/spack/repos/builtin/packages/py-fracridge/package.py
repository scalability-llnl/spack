# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFracridge(PythonPackage):
    """Fractional Ridge Regression."""

    homepage = "https://nrdg.github.io/fracridge"
    pypi = "fracridge/fracridge-1.4.3.tar.gz"
    git = "https://github.com/nrdg/fracridge"

    license("BSD-2-Clause")

    version("2.0", sha256="d49fbffbd58e85da38f572e6ca2ef7563b1a6c8c4e1ab779e2dd207ac944db90")
    version("1.4.3", sha256="0446d486f00fea02110567fd9df14b8b2a7b155dc72700af9201873ea11c27cc")

    depends_on("python@3.7:", when="@2:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"))

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm+toml@3.4:", type=("build", "run"))
    depends_on("py-scikit-learn", when="@2:", type=("build", "run"))
    depends_on("py-scikit-learn@0.23.2", when="@1.4", type=("build", "run"))
    depends_on("py-numba", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
