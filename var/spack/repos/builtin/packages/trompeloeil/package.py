# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Trompeloeil(CMakePackage):
    """Trompeloeil is a thread-safe header-only mocking framework for C++11/14
    using the Boost Software License 1.0"""

    homepage = "https://github.com/rollbear/trompeloeil"
    url = "https://github.com/rollbear/trompeloeil/archive/v43.tar.gz"
    git = "https://github.com/rollbear/trompeloeil.git"

    license("BSL-1.0")

    version("master", branch="master")
    version("47", sha256="4a1d79260c1e49e065efe0817c8b9646098ba27eed1802b0c3ba7d959e4e5e84")
    version("45", sha256="124b0aa45d84415193719376b6557fc1f1180cbfebf4dc4f7ca247cb404d6bd8")
    version("44", sha256="004877db6ba22f24c7867e112e081eeb68858122f55ebe7c7dd9d8d9e3b46c88")
    version("43", sha256="86a0afa2e97347202a0a883ab43da78c1d4bfff0d6cb93205cfc433d0d9eb9eb")

    depends_on("cxx", type="build")  # generated
