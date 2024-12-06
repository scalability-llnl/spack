# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureKeyvault(PythonPackage):
    """Microsoft Azure Key Vault Client Libraries for Python."""

    homepage = (
        "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault"
    )
    pypi = "azure-keyvault/azure-keyvault-4.1.0.zip"

    version("4.1.0", sha256="69002a546921a8290eb54d9a3805cfc515c321bc1d4c0bfcfb463620245eca40")
    version("1.1.0", sha256="37a8e5f376eb5a304fcd066d414b5d93b987e68f9212b0c41efa37d429aadd49")

    depends_on("py-setuptools", type="build")
    depends_on("py-azure-keyvault-certificates@4.1:4", when="@4:", type=("build", "run"))
    depends_on("py-azure-keyvault-secrets@4.1:4", when="@4:", type=("build", "run"))
    depends_on("py-azure-keyvault-keys@4.1:4", when="@4:", type=("build", "run"))
    depends_on("py-msrest@0.5.0:", when="@:1", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", when="@:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", when="@:1", type=("build", "run"))
    depends_on("py-cryptography@2.1.4:", when="@:1", type=("build", "run"))
    depends_on("py-requests@2.18.4:", when="@:1", type=("build", "run"))
