# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestSubprocess(PythonPackage):
    """A plugin to fake subprocess for pytest."""

    homepage = "https://pytest-subprocess.readthedocs.io/en/latest/"
    pypi = "pytest-subprocess/pytest-subprocess-1.5.0.tar.gz"
    git = "https://github.com/aklajnert/pytest-subprocess"

    maintainers("wdconinc")

    license("MIT")

    version("1.5.0", sha256="d7693b96f588f39b84c7b2b5c04287459246dfae6be1dd4098937a728ad4fbe3")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest@4:", type=("build", "run"))
