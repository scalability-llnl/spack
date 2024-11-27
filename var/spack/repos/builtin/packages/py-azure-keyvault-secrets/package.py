# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureKeyvaultSecrets(PythonPackage):
    """Microsoft Azure Key Vault Secrets Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-secrets"
    pypi = "azure-keyvault-secrets/azure-keyvault-secrets-4.1.0.zip"

    version("4.1.0", sha256="4f3bfac60e025e01dd1c1998b73649d45d706975356c0cf147174cf5a6ddf8be")

    depends_on("py-setuptools", type="build")
    depends_on("py-azure-core@1.2.1:1", type=("build", "run"))
    depends_on("py-msrest@0.6.0:", type=("build", "run"))
