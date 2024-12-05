# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestQt(PythonPackage):
    """A pytest plugin that allows programmers to write tests for
    PySide, PySide2 and PyQt applications."""

    homepage = "https://github.com/pytest-dev/pytest-qt"
    pypi = "pytest-qt/pytest-qt-3.3.0.tar.gz"

    license("MIT")

    version("3.3.0", sha256="714b0bf86c5313413f2d300ac613515db3a1aef595051ab8ba2ffe619dbe8925")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-pytest@3:", type=("build", "run"))
