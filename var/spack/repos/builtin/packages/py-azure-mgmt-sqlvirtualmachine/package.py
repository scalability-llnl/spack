# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtSqlvirtualmachine(PythonPackage):
    """Microsoft Azure SQL Virtual Machine Management Client Library for
    Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-sqlvirtualmachine/azure-mgmt-sqlvirtualmachine-0.5.0.zip"

    version("0.5.0", sha256="b5a9423512a7b12844ac014366a1d53c81017a14f39676beedf004a532aa2aad")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
