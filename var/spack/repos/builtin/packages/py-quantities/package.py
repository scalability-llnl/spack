# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQuantities(PythonPackage):
    """Support for physical quantities with units, based on numpy"""

    homepage = "https://python-quantities.readthedocs.org"
    pypi = "quantities/quantities-0.12.1.tar.gz"
    maintainers("apdavison")

    license("DOC")

    version("0.14.1", sha256="efeafffc0c0364f891a9327239cd12496bccb55cd037a6d1bf44de706f722877")
    version("0.13.0", sha256="0fde20115410de21cefa786f3aeae69c1b51bb19ee492190324c1da705e61a81")
    version("0.12.5", sha256="67546963cb2a519b1a4aa43d132ef754360268e5d551b43dd1716903d99812f0")
    version("0.12.4", sha256="a33d636d1870c9e1127631185d89b0105a49f827d6aacd44ad9d8f151f331d8b")

    depends_on("python@3.8:", type=("build", "run"), when="@0.14:")

    depends_on("py-setuptools@61:", type="build", when="@0.14:")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm+toml", type="build", when="@0.14:")

    depends_on("py-numpy@1.19:", type=("build", "run"), when="@0.14:")
    depends_on("py-numpy@1.16:", type=("build", "run"), when="@0.13")
    depends_on("py-numpy@1.8.2:1.17", type=("build", "run"), when="@0.12.4:0.12")
