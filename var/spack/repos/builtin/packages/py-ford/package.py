# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFord(PythonPackage):
    """FORD, standing for FORtran Documenter, is an automatic documentation generator
    for modern Fortran programs."""

    pypi = "FORD/FORD-6.1.11.tar.gz"

    maintainers("wscullin")

    license("GPL-3.0-only")

    version("6.1.13", sha256="95b743ea25c5a9c6a9e13db3633e04f91e11d1debb69f48ca3ef7fefc51f0559")
    version("6.1.12", sha256="101191e1aa33cfe780ea5b2d66d02c7281b9b314e82bb138d76809a49c08506a")
    version("6.1.11", sha256="feb9a88040e717e84c632e4b023904ab36a463fc9a8ff80c8c7f86454e5d8043")

    depends_on("fortran", type="build")  # generated

    depends_on("py-wheel@0.29:", type="build")

    depends_on("py-setuptools@48:", type="build")
    depends_on("py-setuptools-scm@4:5+toml", type="build")
    depends_on("py-setuptools-scm-git-archive", type="build")

    depends_on("py-markdown", type=("build", "run"))
    depends_on("py-markdown-include@0.5.1:", type="run")
    depends_on("py-md-environ", type=("build", "run"), when="@:6.1.8")
    depends_on("py-python-markdown-math@0.8:0", type="run")
    depends_on("py-toposort", type=("build", "run"))
    depends_on("py-jinja2@2.1:", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-beautifulsoup4@4.5.1:", type=("build", "run"))
    depends_on("py-graphviz", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-importlib-metadata", when="^python@:3.7", type=("build", "run"))
