# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiotraj(PythonPackage):
    """Reading structures from trajectory files."""

    homepage = "https://pypi.org/project/biotraj/"
    pypi = "biotraj/biotraj-1.1.0.tar.gz"

    license("LGPL-2.1")

    version("1.2.1", sha256="4d7ad33ad940dbcfb3c2bd228a18f33f88e04657786a9562173b58dc2dd05349")

    depends_on("python@3.10:", type=("build", "run"))

    depends_on("py-setuptools@64:", type=("build", "run"))

    depends_on("py-setuptools-scm@8:", type=("build", "run"))
    depends_on("py-wheel", type=("build", "run"))
    depends_on("py-cython@3.0:", type=("build", "run"))

    depends_on("py-numpy@1.25:", when="@1.2.1", type=("build", "run"))
    depends_on("py-scipy@1.13:", type=("build", "run"))
