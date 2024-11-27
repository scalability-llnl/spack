# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTrojanzooSphinxTheme(PythonPackage):
    """TrojanZoo Sphinx Theme"""

    homepage = "https://github.com/ain-soph/trojanzoo_sphinx_theme"
    pypi = "trojanzoo_sphinx_theme/trojanzoo_sphinx_theme-0.1.0.tar.gz"

    license("GPL-3.0-or-later")

    version("0.1.0", sha256="7b80d70ec84279156dcb9668d3a8a135be1d0d54e20f554fc03ad22d9ff5e7b3")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools@40.9:", type="build")
    depends_on("py-sphinx@4.2:", type=("build", "run"))
    depends_on("py-docutils@0.17.1:", type=("build", "run"))
