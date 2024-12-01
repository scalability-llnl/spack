# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBranca(PythonPackage):
    """Generate complex HTML+JS pages with Python."""

    homepage = "https://python-visualization.github.io/branca"
    pypi = "branca/branca-0.7.1.tar.gz"

    license("MIT")

    version("0.7.1", sha256="e6b6f37a37bc0abffd960c68c045a7fe025d628eff87fedf6ab6ca814812110c")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@41.2:", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-jinja2@3:", type=("build", "run"))
