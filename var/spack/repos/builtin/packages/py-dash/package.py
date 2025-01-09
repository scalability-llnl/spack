# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDash(PythonPackage):
    """Dash is the most downloaded, trusted Python framework
    for building ML & data science web apps."""

    homepage = "https://dash.plotly.com/"
    pypi = "dash/dash-2.17.1.tar.gz"
    git = "https://github.com/plotly/dash.git"

    license("MIT")

    version("2.17.1", sha256="ee2d9c319de5dcc1314085710b72cd5fa63ff994d913bf72979b7130daeea28e")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-typing-extensions")
    depends_on("py-flask")
    depends_on("py-plotly")
    depends_on("py-importlib-metadata")
