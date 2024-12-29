# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMisk(PythonPackage):
    """Miscellaneous useful bits for Python 3."""

    homepage = "https://github.com/marzer/misk"
    url = "https://github.com/marzer/misk/archive/refs/tags/v0.8.1.tar.gz"

    license("MIT", checked_by="pranav-sivaraman")

    version("0.8.1", sha256="35f3cceaefc5f1c3f379b5387a41ef4e57f487ec1b2bc4d8fdde72b2144f0060")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
