# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMultiapiStorage(PythonPackage):
    """Microsoft Azure Storage Client Library for Python with multi API
    version support."""

    homepage = "https://github.com/Azure/azure-multiapi-storage-python"
    pypi = "azure-multiapi-storage/azure-multiapi-storage-0.3.5.tar.gz"

    license("MIT")

    version("0.3.5", sha256="71c238c785786a159b3ffd587a5e7fa1d9a517b66b592ae277fed73a9fbfa2b0")

    depends_on("py-setuptools", type="build")
    depends_on("py-azure-common", type=("build", "run"))
    depends_on("py-cryptography", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-azure-core", type=("build", "run"))
