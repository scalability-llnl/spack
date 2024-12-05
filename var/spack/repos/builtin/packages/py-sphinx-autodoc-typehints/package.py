# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySphinxAutodocTypehints(PythonPackage):
    """
    Type hints (PEP 484) support for the Sphinx autodoc extension
    """

    homepage = "https://github.com/agronholm/sphinx-autodoc-typehints"
    pypi = "sphinx-autodoc-typehints/sphinx-autodoc-typehints-1.12.0.tar.gz"

    license("MIT")

    version("1.12.0", sha256="193617d9dbe0847281b1399d369e74e34cd959c82e02c7efde077fca908a9f52")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@40.0.4:", type="build")
    depends_on("py-setuptools-scm@2.0.0:", type="build")
    depends_on("py-sphinx@3:", type=("build", "run"))
