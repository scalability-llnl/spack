# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestDatadir(PythonPackage):
    """Pytest plugin for manipulating test data directories and files."""

    homepage = "https://github.com/gabrielcnr/pytest-datadir"
    pypi = "pytest-datadir/pytest-datadir-1.4.1.tar.gz"
    maintainers("HaoZeke")

    license("MIT")

    version("1.4.1", sha256="9f7a3c4def6ac4cac3cc8181139ab53bd2667231052bd40cb07081748d4420f0")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-pytest@5.0:", type=("build", "run"))
