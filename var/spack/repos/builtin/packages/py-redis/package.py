# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRedis(PythonPackage):
    """The Python interface to the Redis key-value store."""

    homepage = "https://github.com/redis/redis-py"
    pypi = "redis/redis-3.3.8.tar.gz"

    license("MIT")

    version("4.5.1", sha256="1eec3741cda408d3a5f84b78d089c8b8d895f21b3b050988351e925faf202864")
    version("3.5.3", sha256="0e7e0cfca8660dea8b7d5cd8c4f6c5e29e11f31158c0b0ae91a397f00e5a05a2")
    version("3.5.0", sha256="7378105cd8ea20c4edc49f028581e830c01ad5f00be851def0f4bc616a83cd89")
    version("3.3.8", sha256="98a22fb750c9b9bb46e75e945dc3f61d0ab30d06117cbb21ff9cd1d315fedd3b")

    variant(
        "hiredis",
        default=False,
        description="Support for hiredis which speeds up parsing of multi bulk replies",
    )

    depends_on("py-setuptools", type="build")
    depends_on("py-importlib-metadata@1:", when="@4: ^python@:3.7", type=("build", "run"))
    depends_on("py-typing-extensions", when="@4: ^python@:3.7", type=("build", "run"))
    depends_on("py-async-timeout@4.0.2:", when="@4:", type=("build", "run"))

    depends_on("py-hiredis@1:", when="@4: +hiredis", type=("build", "run"))
    depends_on("py-hiredis@0.1.3:", when="+hiredis", type=("build", "run"))
