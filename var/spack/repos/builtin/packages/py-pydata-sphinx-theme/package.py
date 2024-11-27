# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydataSphinxTheme(PythonPackage):
    """A clean, three-column, Bootstrap-based Sphinx theme by and for the PyData community."""

    homepage = "https://pydata-sphinx-theme.readthedocs.io/en/stable"
    pypi = "pydata_sphinx_theme/pydata_sphinx_theme-0.14.1.tar.gz"

    license("BSD-3-Clause")

    version("0.14.1", sha256="d8d4ac81252c16a002e835d21f0fea6d04cf3608e95045c816e8cc823e79b053")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-sphinx-theme-builder", type="build")

    depends_on("py-sphinx@5:", type=("build", "run"))
    depends_on("py-beautifulsoup4", type=("build", "run"))
    depends_on("py-docutils@:0.16,0.17.1:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-babel", type=("build", "run"))
    depends_on("py-pygments@2.7:", type=("build", "run"))
    depends_on("py-accessible-pygments", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
