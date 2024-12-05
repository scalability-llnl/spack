# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySmmap(PythonPackage):
    """
    A pure Python implementation of a sliding window memory map manager
    """

    homepage = "https://github.com/gitpython-developers/smmap"
    pypi = "smmap/smmap-3.0.4.tar.gz"

    license("BSD-3-Clause")

    version("5.0.0", sha256="c840e62059cd3be204b0c9c9f74be2c09d5648eddd4580d9314c3ecde0b30936")
    version("4.0.0", sha256="7e65386bd122d45405ddf795637b7f7d2b532e7e401d46bbe3fb49b9986d5182")
    version("3.0.5", sha256="84c2751ef3072d4f6b2785ec7ee40244c6f45eb934d9e543e2c51f1bd3d54c50")
    version("3.0.4", sha256="9c98bbd1f9786d22f14b3d4126894d56befb835ec90cef151af566c7e19b5d24")

    depends_on("python@3.6:", type=("build", "run"), when="@5.0.0:")
    depends_on("python@3.5:", type=("build", "run"), when="@4.0.0")
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"), when="@:3")
    depends_on("py-setuptools", type="build")
