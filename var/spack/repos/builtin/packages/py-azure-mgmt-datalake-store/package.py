# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtDatalakeStore(PythonPackage):
    """Microsoft Azure Data Lake Store Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-datalake-store/azure-mgmt-datalake-store-0.5.0.zip"

    version("0.5.0", sha256="9376d35495661d19f8acc5604f67b0bc59493b1835bbc480f9a1952f90017a4c")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrestazure@0.4.27:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
