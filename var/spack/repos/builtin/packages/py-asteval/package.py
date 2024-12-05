# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsteval(PythonPackage):
    """Safe, minimalistic evaluator of python expression using ast module"""

    homepage = "https://github.com/newville/asteval"
    pypi = "asteval/asteval-0.9.18.tar.gz"

    license("MIT")

    version("0.9.25", sha256="bea22b7d8fa16bcba95ebc72052ae5d8ca97114c9959bb47f8b8eebf30e4342f")
    version("0.9.18", sha256="5d64e18b8a72c2c7ae8f9b70d1f80b68bbcaa98c1c0d7047c35489d03209bc86")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@0.9.25:")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build", when="@0.9.25:")
