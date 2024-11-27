# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPytestMpi(PythonPackage):
    """Pytest plugin to collect information from tests."""

    homepage = "https://pytest-mpi.readthedocs.io"
    pypi = "pytest-mpi/pytest-mpi-0.6.tar.gz"

    license("BSD-3-Clause")

    maintainers("tristan0x")

    version("0.6", sha256="09b3cd3511f8f3cd4d205f54d4a7223724fed0ab68b872ed1123d312152325a9")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-pytest@3.4:", type=("build", "run"))
