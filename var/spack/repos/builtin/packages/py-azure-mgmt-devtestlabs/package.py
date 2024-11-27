# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtDevtestlabs(PythonPackage):
    """Microsoft Azure DevTestLabs Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-devtestlabs/azure-mgmt-devtestlabs-4.0.0.zip"

    version("4.0.0", sha256="59549c4c4068f26466b1097b574a8e5099fb2cd6c8be0a00395b06d3b29e278d")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
