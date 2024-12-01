# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAiohttpCors(PythonPackage):
    """aiohttp_cors library implements Cross Origin Resource Sharing (CORS)
    support for aiohttp asyncio-powered asynchronous HTTP server."""

    homepage = "https://github.com/aio-libs/aiohttp-cors"
    pypi = "aiohttp_cors/aiohttp-cors-0.7.0.tar.gz"

    license("Apache-2.0")

    version("0.7.0", sha256="4d39c6d7100fd9764ed1caf8cebf0eb01bf5e3f24e2e073fda6234bc48b19f5d")

    depends_on("python@3.4.1:", type=("build", "run"))
    depends_on("py-setuptools@20.8.1:", type="build")
    depends_on("py-aiohttp@1.1:", type=("build", "run"))
