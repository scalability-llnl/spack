# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestParallel(PythonPackage):
    """A pytest plugin for parallel and concurrent testing."""

    homepage = "https://github.com/browsertron/pytest-parallel"
    pypi = "pytest-parallel/pytest-parallel-0.1.1.tar.gz"

    license("MIT")

    version("0.1.1", sha256="9aac3fc199a168c0a8559b60249d9eb254de7af58c12cee0310b54d4affdbfab")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pytest@3.0:", type=("build", "run"))
    depends_on("py-tblib", type=("build", "run"))
