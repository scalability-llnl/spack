# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureStorageCommon(PythonPackage):
    """Microsoft Azure Storage Common Client Library for Python."""

    homepage = "https://github.com/Azure/azure-storage-python"
    pypi = "azure-storage-common/azure-storage-common-2.1.0.tar.gz"

    license("MIT")

    version("2.1.0", sha256="ccedef5c67227bc4d6670ffd37cec18fb529a1b7c3a5e53e4096eb0cf23dc73f")
    version("1.4.2", sha256="4ec87c7537d457ec95252e0e46477e2c1ccf33774ffefd05d8544682cb0ae401")

    depends_on("py-setuptools", type="build")
    depends_on("py-azure-common@1.1.5:", type=("build", "run"))
    depends_on("py-cryptography", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
