# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPylatex(PythonPackage):
    """A Python library for creating LaTeX files and snippets"""

    homepage = "https://github.com/JelteF/PyLaTeX"
    pypi = "PyLaTeX/PyLaTeX-1.4.1.tar.gz"

    license("MIT")

    version("1.4.1", sha256="d3c12efb8b260771260443dce78d1e9089c09f9d0b92e6273dfca0bf5e7302fb")

    variant("docs", default=False, description="Build with Sphinx support for documentation")
    variant("matrices", default=False, description="Build with matrix support")
    variant("matplotlib", default=False, description="Build with matplotlib support")
    variant("quantities", default=False, description="Build with quantities support")

    depends_on("python@2.7,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@:57", type="build", when="@:1.4.1")
    depends_on("py-ordered-set", type=("build", "run"))

    # from extras section in setup.py
    depends_on("py-sphinx", type="run", when="+docs")
    depends_on("py-matplotlib", type="run", when="+matplotlib")
    depends_on("py-numpy", type="run", when="+matrices")
    depends_on("py-numpy", type="run", when="+quantities")
    depends_on("py-quantities", type="run", when="+quantities")

    depends_on("texlive", type="run")
