# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtBilling(PythonPackage):
    """Microsoft Azure Billing Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-billing/azure-mgmt-billing-0.2.0.zip"

    version("0.2.0", sha256="85f73bb3808a7d0d2543307e8f41e5b90a170ad6eeedd54fe7fcaac61b5b22d2")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrestazure@0.4.20:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
