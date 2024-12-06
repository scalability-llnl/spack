# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtCosmosdb(PythonPackage):
    """Microsoft Azure Cosmos DB Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-cosmosdb/azure-mgmt-cosmosdb-0.15.0.zip"

    version("0.15.0", sha256="e70fe9b3d9554c501d46e69f18b73de18d77fbcb98a7a87b965b3dd027cada0f")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
