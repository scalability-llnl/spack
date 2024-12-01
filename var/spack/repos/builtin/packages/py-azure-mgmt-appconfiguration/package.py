# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtAppconfiguration(PythonPackage):
    """Microsoft Azure App Configuration Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-appconfiguration/azure-mgmt-appconfiguration-0.5.0.zip"

    version("0.5.0", sha256="211527511d7616a383cc196956eaf2b7ee016f2367d367924b3715f2a41106da")
    version("0.4.0", sha256="85f6202ba235fde6be274f3dec1578b90235cf31979abea3fcfa476d0b2ac5b6")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
