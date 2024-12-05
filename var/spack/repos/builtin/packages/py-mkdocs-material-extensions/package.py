# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocsMaterialExtensions(PythonPackage):
    """Markdown extension resources for MkDocs for Material."""

    homepage = "https://github.com/facelessuser/mkdocs-material-extensions"
    pypi = "mkdocs-material-extensions/mkdocs-material-extensions-1.0.3.tar.gz"

    license("MIT")

    version("1.0.3", sha256="bfd24dfdef7b41c312ede42648f9eb83476ea168ec163b613f9abd12bbfddba2")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
