# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtDns(PythonPackage):
    """Microsoft Azure DNS Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-dns/azure-mgmt-dns-3.0.0.zip"

    version("3.0.0", sha256="6ecdf4e67d8eb5db593ec331e6d9f350616e77c31225c91d266605e03e63b37f")
    version("2.1.0", sha256="3730b1b3f545a5aa43c0fff07418b362a789eb7d81286e2bed90ffef88bfa5d0")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
