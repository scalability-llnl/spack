# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestForked(PythonPackage):
    """Run tests in isolated forked subprocesses."""

    homepage = "https://github.com/pytest-dev/pytest-forked"
    pypi = "pytest-forked/pytest-forked-1.1.1.tar.gz"

    license("MIT")

    version("1.1.1", sha256="e2d46f319c8063a3a0536b18f9cdea6eea3bc9fe2cb16c94e1d6fad3abc37300")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-pytest@3.1.0:", type=("build", "run"))
