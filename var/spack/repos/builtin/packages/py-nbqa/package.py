# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNbqa(PythonPackage):
    """Run any standard Python code quality tool on a Jupyter Notebook."""

    homepage = "https://github.com/nbQA-dev/nbQA"
    pypi = "nbqa/nbqa-1.6.3.tar.gz"

    license("MIT")

    version("1.6.3", sha256="5394a29fc6d27b9a950c0a36d2d9de25de980be9acfe2a3f3aea0d27b5f7fec1")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-ipython@7.8:", type=("build", "run"))
    depends_on("py-tokenize-rt@3.2:", type=("build", "run"))
    depends_on("py-tomli", type=("build", "run"))
