# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtRelay(PythonPackage):
    """Microsoft Azure Relay Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-relay/azure-mgmt-relay-0.2.0.zip"

    version("0.2.0", sha256="a7e8341b2920d1d45bdf73d2b7825c44427d33fb0d820aceb11c94432323bf68")
    version("0.1.0", sha256="d9f987cf2998b8a354f331b2a71082c049193f1e1cd345812e14b9b821365acb")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", when="@0.2:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", when="@0.2:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.20:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
