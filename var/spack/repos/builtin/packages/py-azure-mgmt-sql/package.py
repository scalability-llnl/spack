# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtSql(PythonPackage):
    """Microsoft Azure SQL Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-sql/azure-mgmt-sql-0.19.0.zip"

    version("0.19.0", sha256="694649d4c9c5f89e543f23ec10e450b6382b2f1bc5843ef266cfc302276038c6")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
