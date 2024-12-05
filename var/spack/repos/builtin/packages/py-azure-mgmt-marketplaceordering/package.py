# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtMarketplaceordering(PythonPackage):
    """Microsoft Azure Market Place Ordering Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-marketplaceordering/azure-mgmt-marketplaceordering-0.2.1.zip"

    version("0.2.1", sha256="dc765cde7ec03efe456438c85c6207c2f77775a8ce8a7adb19b0df5c5dc513c2")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
