# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtNetwork(PythonPackage):
    """Microsoft Azure Network Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-network/azure-mgmt-network-11.0.0.zip"

    version("11.0.0", sha256="7fdfc631c660cb173eee88abbb7b8be7742f91b522be6017867f217409cd69bc")
    version("10.2.0", sha256="d50c74cdc1c9be6861ddef9adffd3b05afc5a5092baf0209eea30f4439cba2d9")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
