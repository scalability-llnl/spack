# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxImmaterial(PythonPackage):
    """An adaptation of the popular mkdocs-material theme for the Sphinx documentation tool."""

    homepage = "https://github.com/jbms/sphinx-immaterial"
    pypi = "sphinx_immaterial/sphinx_immaterial-0.11.2.tar.gz"

    license("MIT")

    version("0.11.2", sha256="a1c8387ca8b4da282949e474647d06f3b2f7d12fe54e9e662b962771012bf257")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@6.3.2:", type="build")
    depends_on("py-appdirs", type=("build", "run"))
    depends_on("py-markupsafe", type=("build", "run"))
    depends_on("py-pydantic", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-sphinx@4:", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))

    # see https://jbms.github.io/sphinx-immaterial/#material-for-sphinx for node requirements
    depends_on("node-js@14:", type="build")
    depends_on("npm", type="build")
