# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestFilterSubpackage(PythonPackage):
    """Pytest plugin for filtering based on sub-packages."""

    homepage = "https://github.com/astropy/pytest-filter-subpackage"
    pypi = "pytest-filter-subpackage/pytest-filter-subpackage-0.1.2.tar.gz"

    license("BSD-3-Clause")

    version("0.1.2", sha256="1faea36717803e524588d6c109d26d20d3b34422e8d6a96812758977dca01782")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-pytest@3:", type=("build", "run"))
