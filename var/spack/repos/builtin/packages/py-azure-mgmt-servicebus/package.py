# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtServicebus(PythonPackage):
    """Microsoft Azure Service Bus Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-servicebus/azure-mgmt-servicebus-0.6.0.zip"

    version("0.6.0", sha256="f20920b8fb119ef4abeda4d2dac765a4fc48cd0bcf30c27f8c4cc6d890bc08b1")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
