# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMock(PythonPackage):
    """mock is a library for testing in Python. It allows you to replace parts
    of your system under test with mock objects and make assertions about how
    they have been used."""

    homepage = "https://github.com/testing-cabal/mock"
    pypi = "mock/mock-4.0.3.tar.gz"

    license("BSD-2-Clause")

    version("4.0.3", sha256="7d3fbbde18228f4ff2f1f119a45cdffa458b4c0dee32eb4d2bb2f82554bac7bc")
    version("3.0.5", sha256="83657d894c90d5681d62155c82bda9c1187827525880eda8ff5df4ec813437c3")
    version("3.0.3", sha256="5eda46efb363128828d6fd2bf8d16f6ebb66f5b543b9f7f8f4eb224c5cb503fe")
    version("2.0.0", sha256="b158b6df76edd239b8208d481dc46b6afd45a846b7812ff0ce58971cf5bc8bba")
    version("1.3.0", sha256="1e247dbecc6ce057299eb7ee019ad68314bb93152e81d9a6110d35f4d5eca0f6")

    depends_on("python@3.6:", type=("build", "run"), when="@3")
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"), when="@:2")
    depends_on("py-setuptools@17.1:", type="build")
    depends_on("py-pbr@1.3:", type=("build"), when="@:2")
    depends_on("py-six@1.9:", type=("build", "run"), when="@:2")
