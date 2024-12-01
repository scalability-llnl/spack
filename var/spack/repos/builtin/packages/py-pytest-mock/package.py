# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestMock(PythonPackage):
    """Thin-wrapper around the mock package for easier use with py.test"""

    homepage = "https://github.com/pytest-dev/pytest-mock"
    pypi = "pytest-mock/pytest-mock-1.11.1.tar.gz"

    maintainers("thomas-bouvier")

    license("MIT")

    version("3.10.0", sha256="fbbdb085ef7c252a326fd8cdcac0aa3b1333d8811f131bdcc701002e1be7ed4f")
    version("1.11.1", sha256="f1ab8aefe795204efe7a015900296d1719e7bf0f4a0558d71e8599da1d1309d0")
    version(
        "1.2",
        sha256="f78971ed376fcb265255d1e4bb313731b3a1be92d7f3ecb19ea7fedc4a56fd0f",
        url="https://pypi.io/packages/source/p/pytest-mock/pytest-mock-1.2.zip",
    )

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"), when="@:1.11.1")
    depends_on("python@3.7:", type=("build", "run"), when="@3.10.0:")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-pytest@2.7:", type=("build", "run"))
    depends_on("py-pytest@5:", type=("build", "run"), when="@3.10.0:")
