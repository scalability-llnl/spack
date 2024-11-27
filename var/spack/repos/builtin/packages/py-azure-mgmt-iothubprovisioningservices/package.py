# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtIothubprovisioningservices(PythonPackage):
    """Microsoft Azure IoTHub Provisioning Services Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-iothubprovisioningservices/azure-mgmt-iothubprovisioningservices-0.2.0.zip"

    version("0.2.0", sha256="8c37acfd1c33aba845f2e0302ef7266cad31cba503cc990a48684659acb7b91d")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrestazure@0.4.20:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
