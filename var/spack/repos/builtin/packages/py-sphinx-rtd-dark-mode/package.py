# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxRtdDarkMode(PythonPackage):
    """A Sphinx extension for adding a toggleable dark mode to the Read the Docs theme."""

    homepage = "https://github.com/MrDogeBro/sphinx_rtd_dark_mode"
    pypi = "sphinx-rtd-dark-mode/sphinx_rtd_dark_mode-1.2.4.tar.gz"

    license("MIT")

    version("1.2.4", sha256="935bc1f3e62fc76eadd7d2760ac7f48bab907a97e44beda749a48a2706aeed63")

    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx-rtd-theme", type=("build", "run"))
    depends_on("python@3.4:", type=("build", "run"))
