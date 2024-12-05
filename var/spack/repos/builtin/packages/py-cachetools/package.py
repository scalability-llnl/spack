# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCachetools(PythonPackage):
    """This module provides various memoizing collections and decorators,
    including variants of the Python 3 Standard Library @lru_cache function
    decorator."""

    homepage = "https://github.com/tkem/cachetools"
    pypi = "cachetools/cachetools-3.1.1.tar.gz"

    license("MIT")

    version("5.2.0", sha256="6a94c6402995a99c3970cc7e4884bb60b4a8639938157eeed436098bf9831757")
    version("4.2.4", sha256="89ea6f1b638d5a73a4f9226be57ac5e4f399d22770b92355f92dcb0f7f001693")
    version("4.2.2", sha256="61b5ed1e22a0924aed1d23b478f37e8d52549ff8a961de2909c69bf950020cff")
    version("3.1.1", sha256="8ea2d3ce97850f31e4a08b0e2b5e6c34997d7216a9d2c98e0f3978630d4da69a")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@46.4.0:", when="@4.2.2:", type="build")
    depends_on("python@3.5:3", when="@4.2.2", type=("build", "run"))
    depends_on("python@3.7:3", when="@5.2.0", type=("build", "run"))
