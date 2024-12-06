# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestCov(PythonPackage):
    """Pytest plugin for measuring coverage."""

    homepage = "https://github.com/pytest-dev/pytest-cov"
    pypi = "pytest-cov/pytest-cov-2.8.1.tar.gz"

    license("MIT")

    version("4.0.0", sha256="996b79efde6433cdbd0088872dbc5fb3ed7fe1578b68cdbba634f14bb8dd0470")
    version("3.0.0", sha256="e7f0f5b1617d2210a2cabc266dfe2f4c75a8d32fb89eafb7ad9d06f6d076d470")
    version("2.8.1", sha256="cc6742d8bac45070217169f5f72ceee1e0e55b0221f54bcf24845972d3a47f2b")
    version("2.3.1", sha256="fa0a212283cdf52e2eecc24dd6459bb7687cc29adb60cb84258fab73be8dda0f")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest@4.6:", when="@3:", type=("build", "run"))
    depends_on("py-pytest@3.6:", type=("build", "run"))
    depends_on("py-coverage@5.2.1: +toml", when="@3:", type=("build", "run"))
    depends_on("py-coverage@4.4:", type=("build", "run"))
