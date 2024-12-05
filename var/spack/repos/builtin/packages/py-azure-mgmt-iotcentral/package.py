# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtIotcentral(PythonPackage):
    """Microsoft Azure IoTCentral Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-iotcentral/azure-mgmt-iotcentral-3.1.0.zip"

    version("3.1.0", sha256="c175f6642be514ad0efd3dc03d09e50d923596fd9e634381793dcc46bb8a57c7")
    version("3.0.0", sha256="f6dacf442ccae2f18f1082e80bcbdcaa8c0efa2ba92b48c5db6ee01d37240047")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
