# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsyncio(PythonPackage):
    """The asyncio module provides infrastructure for writing
    single-threaded concurrent code using coroutines, multiplexing I/O
    access over sockets and other resources, running network clients
    and servers, and other related primitives."""

    homepage = "https://docs.python.org/3/library/asyncio.html"
    url = "https://github.com/python/asyncio/archive/3.4.3.tar.gz"

    license("Apache-2.0")

    version("3.4.3", sha256="b22225680ea04c3528b7fa03e9c6d152470173dd3873996b8cb29fcb37799f1b")
    version("3.4.2", sha256="ba28d351c579875e2a1cb1989e310285d3eb76c5bb749694b6ddd3901f8d39de")
    version("3.4.1", sha256="51cdfbd4964ef8286cbef7d88f9b7abcc8b710ecec0a0794aa354f94ef703126")

    depends_on("c", type="build")  # generated

    depends_on("python@3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
