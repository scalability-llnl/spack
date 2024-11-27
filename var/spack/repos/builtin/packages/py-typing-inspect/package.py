# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypingInspect(PythonPackage):
    """Runtime inspection utilities for typing module."""

    homepage = "https://github.com/ilevkivskyi/typing_inspect"
    pypi = "typing_inspect/typing_inspect-0.8.0.tar.gz"

    license("MIT")

    version("0.8.0", sha256="8b1ff0c400943b6145df8119c41c244ca8207f1f10c9c057aeed1560e4806e3d")

    depends_on("py-setuptools", type="build")
    depends_on("py-mypy-extensions@0.3:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", type=("build", "run"))
