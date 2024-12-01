# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtAuthorization(PythonPackage):
    """Microsoft Azure Authorization Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-authorization/azure-mgmt-authorization-0.60.0.zip"

    version("0.60.0", sha256="31e875a34ac2c5d6fefe77b4a8079a8b2bdbe9edb957e47e8b44222fb212d6a7")
    version("0.52.0", sha256="16a618c4357c11e96de376856c396f09e76a56473920cdf7a66735fabaa2a70c")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
