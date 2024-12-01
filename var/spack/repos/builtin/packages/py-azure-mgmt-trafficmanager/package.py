# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtTrafficmanager(PythonPackage):
    """Microsoft Azure Traffic Manager Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-trafficmanager/azure-mgmt-trafficmanager-0.51.0.zip"

    version("0.51.0", sha256="fc8ae77022cfe52fda4379a2f31e0b857574d536e41291a7b569b5c0f4104186")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
