# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAsyncTimeout(PythonPackage):
    """asyncio-compatible timeout context manager."""

    homepage = "https://github.com/aio-libs/async-timeout"
    pypi = "async-timeout/async-timeout-3.0.1.tar.gz"

    license("Apache-2.0")

    version("4.0.2", sha256="2163e1640ddb52b7a8c80d0a67a08587e5d245cc9c553a74a847056bc2976b15")
    version("4.0.1", sha256="b930cb161a39042f9222f6efb7301399c87eeab394727ec5437924a36d6eef51")
    version("4.0.0", sha256="7d87a4e8adba8ededb52e579ce6bc8276985888913620c935094c2276fd83382")
    version("3.0.1", sha256="0c3c816a028d47f659d6ff5c745cb2acf1f966da1fe5c19c77a70282b25f4c5f")

    depends_on("py-setuptools@45:", type="build")
    depends_on("python@3.5.3:", type=("build", "run"), when="@3.0.1:")
    depends_on("python@3.6:", type=("build", "run"), when="@4.0.1:")
    depends_on("py-typing-extensions@3.6.5:", type=("build", "run"), when="@4.0.1")
    depends_on("py-typing-extensions@3.6.5:", type=("build", "run"), when="@4.0.2: ^python@:3.7")
