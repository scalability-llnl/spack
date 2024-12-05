# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureKeyvaultKeys(PythonPackage):
    """Microsoft Azure Key Vault Keys Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-keys"
    pypi = "azure-keyvault-keys/azure-keyvault-keys-4.1.0.zip"

    version("4.1.0", sha256="f9967b4deb48e619f6c40558f69e48978779cc09c8a7fad33d536cfc41cd68f9")

    depends_on("py-setuptools", type="build")
    depends_on("py-azure-core@1.2.1:1", type=("build", "run"))
    depends_on("py-cryptography@2.1.4:", type=("build", "run"))
    depends_on("py-msrest@0.6.0:", type=("build", "run"))
