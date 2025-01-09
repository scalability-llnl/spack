# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFalcon(PythonPackage):
    """Falcon is a reliable, high-performance Python web framework for
    building large-scale app backends and microservices."""

    homepage = "https://github.com/falconry/falcon"
    url = "https://github.com/falconry/falcon/archive/refs/tags/3.0.0a2.tar.gz"

    license("Apache-2.0")

    version("3.0.0a2", sha256="2e8471cf07df33a1b9929de8953aeb301c64a963c86d770ef296ce4dc8af34cd")
    version("3.0.0a1", sha256="cdc47996f664fa8c97041a2a4a586a472442654ee7e86075bb72c720744150ca")
    version("2.0.0rc4", sha256="30bb6a982cf3ab273b9605c9d2ab1e7d01323fee13fe53a485befd92186c3665")
    version("2.0.0rc3", sha256="0e76d142ff00dd097b0dc19c58b052e23c5cc81a148bfffa04768c83e77b66b9")
    version("2.0.0rc2", sha256="b3f154aec8e64c3b196c3279b9dd824ed9457d6bd7bac23578948e34c9b2ec83")
    version("2.0.0rc1", sha256="4ca3a304b28be4b324efc58c9f2af9c6babb26479837f93e183d95f0aff7dbd0")
    version("2.0.0b2", sha256="ec9526b8a2ec5f25164fe882b7c3c466cda0de179b211be7fd1f5ad65dad398c")
    version("2.0.0b1", sha256="7e6e28a2c2cacb9e5731790af70d4305fc1bfc484721e0696dece83c4f240722")
    version("2.0.0a2", sha256="a0b6e089c604b5104bc8b8516f7ddce1c4c10690896e2dac833fcb84a34e7257")
    version("2.0.0", sha256="4cdd99706061967bdcd756fe5f474915fedb5ddf4be16fbd25d8456ededa1e9d")

    depends_on("python", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type=("build", "run"))
