# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureCosmos(PythonPackage):
    """Microsoft Azure Cosmos Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-cosmos/azure-cosmos-4.0.0.zip"

    license("MIT")

    version("4.0.0", sha256="c4e40e0d378fd0c96664f46f1ad08e6c8aaaac31c463726a74aae9eae724442d")
    version(
        "3.2.0",
        sha256="4f77cc558fecffac04377ba758ac4e23f076dc1c54e2cf2515f85bc15cbde5c6",
        url="https://pypi.io/packages/source/a/azure-cosmos/azure-cosmos-3.2.0.tar.gz",
    )

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.6:", type=("build", "run"))
    depends_on("py-azure-core@1.0.0:1", when="@4:", type=("build", "run"))
    depends_on("py-requests@2.10.0:", when="@:3", type=("build", "run"))
