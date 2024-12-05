# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureKeyvaultNspkg(PythonPackage):
    """Microsoft Azure Key Vault Namespace Package."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault"
    pypi = "azure-keyvault-nspkg/azure-keyvault-nspkg-1.0.0.zip"

    version("1.0.0", sha256="ac68b88aab9c6caf54a23da2a1d1c718d7520bae5adff04dd0a743228269b641")

    depends_on("py-setuptools", type="build")
    depends_on("py-azure-nspkg@3.0.0:", type=("build", "run"))
