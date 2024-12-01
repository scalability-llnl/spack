# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtRedis(PythonPackage):
    """Microsoft Azure Redis Cache Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-redis/azure-mgmt-redis-6.0.0.zip"

    # Release candidate needed for py-azure-cli
    version("7.0.0rc1", sha256="d3cc259c507b79962495ed00d0a3432a45e4e90a0fb48b49e80d51cdc398dc20")
    version(
        "6.0.0",
        sha256="db999e104edeee3a13a8ceb1881e15196fe03a02635e0e20855eb52c1e2ecca1",
        preferred=True,
    )

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
