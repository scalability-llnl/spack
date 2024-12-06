# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtApimanagement(PythonPackage):
    """Microsoft Azure API Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-apimanagement/azure-mgmt-apimanagement-0.2.0.zip"

    version("0.2.0", sha256="790f01c0b32583706b8b8c59667c0f5a51cd70444eee76474e23a598911e1d72")
    version("0.1.0", sha256="5d45d3438c6a11bae6bb8d4d5173cdb44b85683695f9f3433f22f45aecc47819")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
