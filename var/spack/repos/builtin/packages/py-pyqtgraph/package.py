# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqtgraph(PythonPackage):
    """PyQtGraph is a pure-python graphics and GUI library intended for use in mathematics,
    scientific, and engineering applications"""

    homepage = "https://www.pyqtgraph.org/"
    pypi = "pyqtgraph/pyqtgraph-0.13.3.tar.gz"

    license("MIT", checked_by="A-N-Other")

    version("0.13.3", sha256="58108d8411c7054e0841d8b791ee85e101fc296b9b359c0e01dde38a98ff2ace")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.20:", type=("build", "run"))
    # This dependency listed in README.md ...
    depends_on("py-pyqt6", type=("build", "run"))
