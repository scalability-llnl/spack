# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMike(PythonPackage):
    """mike is a Python utility to easily deploy multiple versions of your
    MkDocs-powered docs to a Git branch, suitable for deploying to Github
    via gh-pages."""

    homepage = "https://github.com/jimporter/mike"
    pypi = "mike/mike-1.1.2.tar.gz"

    license("BSD-3-Clause")

    version("1.1.2", sha256="56c3f1794c2d0b5fdccfa9b9487beb013ca813de2e3ad0744724e9d34d40b77b")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-mkdocs@1.0:", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-pyyaml@5.1:", type=("build", "run"))
    depends_on("py-verspec", type=("build", "run"))
