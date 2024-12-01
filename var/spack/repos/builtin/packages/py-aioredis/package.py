# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAioredis(PythonPackage):
    """asyncio (PEP 3156) Redis support."""

    homepage = "https://github.com/aio-libs/aioredis"
    pypi = "aioredis/aioredis-1.3.1.tar.gz"

    license("MIT")

    version("1.3.1", sha256="15f8af30b044c771aee6787e5ec24694c048184c7b9e54c3b60c750a4b93273a")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-async-timeout", type=("build", "run"))
    depends_on("py-hiredis", type=("build", "run"))
