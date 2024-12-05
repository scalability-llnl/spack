# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtDeploymentmanager(PythonPackage):
    """Microsoft Azure Deployment Manager Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-deploymentmanager/azure-mgmt-deploymentmanager-0.2.0.zip"

    version("0.2.0", sha256="46e342227993fc9acab1dda42f2eb566b522a8c945ab9d0eea56276b46f6d730")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
