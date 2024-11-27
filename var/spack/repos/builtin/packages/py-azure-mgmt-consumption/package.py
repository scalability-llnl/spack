# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtConsumption(PythonPackage):
    """Microsoft Azure Consumption Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-consumption/azure-mgmt-consumption-3.0.0.zip"

    version("3.0.0", sha256="035d4b74ca7c47e2683bea17105fd9014c27060336fb6255324ac86b27f70f5b")
    version("2.0.0", sha256="9a85a89f30f224d261749be20b4616a0eb8948586f7f0f20573b8ea32f265189")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", when="@3:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", when="@3:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.20:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
