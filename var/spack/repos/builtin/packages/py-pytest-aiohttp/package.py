# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestAiohttp(PythonPackage):
    """Pytest plugin for aiohttp support."""

    homepage = "https://github.com/aio-libs/pytest-aiohttp"
    pypi = "pytest-aiohttp/pytest-aiohttp-1.0.5.tar.gz"

    license("Apache-2.0")

    version("1.0.5", sha256="880262bc5951e934463b15e3af8bb298f11f7d4d3ebac970aab425aff10a780a")

    depends_on("py-setuptools@51.0:", type="build")
    depends_on("py-setuptools-scm@6.2:", type="build")
    depends_on("py-wheel@0.36:", type="build")

    depends_on("py-pytest@6.1.0:", type=("build", "run"))
    depends_on("py-aiohttp@3.8.1:", type=("build", "run"))
    depends_on("py-pytest-asyncio@0.17.2:", type=("build", "run"))
