# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestRegtest(PythonPackage):
    """pytest plugin for snapshot regression testing."""

    homepage = "https://gitlab.com/uweschmitt/pytest-regtest"
    pypi = "pytest_regtest/pytest_regtest-2.1.1.tar.gz"

    license("MIT")

    version("2.1.1", sha256="bd08a6161832378b59ecd4f5815fbe26af7cd091db4a1e710e30476d5f3b8832")

    depends_on("py-hatchling", type="build")
    depends_on("py-pytest@7.3:", type=("build", "run"))
