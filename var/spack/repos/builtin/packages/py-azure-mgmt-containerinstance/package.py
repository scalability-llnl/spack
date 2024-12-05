# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtContainerinstance(PythonPackage):
    """Microsoft Azure Container Instance Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-containerinstance/azure-mgmt-containerinstance-2.0.0.zip"

    version("2.0.0", sha256="5ad247d186c3c040da7a1d40ad39c9881e99afc58271f673abb602abb0b6b85b")
    version("1.5.0", sha256="b055386f04ba8433112b0df7fcbc260b5208828d7bb8c057e760fe596aa7a8cd")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
