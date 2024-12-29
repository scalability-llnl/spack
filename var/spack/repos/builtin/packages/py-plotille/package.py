# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPlotille(PythonPackage):
    """Plot in the terminal using braille dots."""

    homepage = "https://github.com/tammoippen/plotille"
    pypi = "plotille/plotille-5.0.0.tar.gz"
    git = "https://github.com/tammoippen/plotille.git"

    version("5.0.0", sha256="99e5ca51a2e4c922ead3a3b0863cc2c6a9a4b3f701944589df10f42ce02ab3dc")

    license("MIT")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
