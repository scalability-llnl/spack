# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtNetapp(PythonPackage):
    """Microsoft Azure NetApp Files Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-netapp/azure-mgmt-netapp-0.11.0.zip"

    version("0.11.0", sha256="621a76b06c97e858d49b68953e66eb718ac24f91aa6bf090f32a335a38f02305")
    version("0.8.0", sha256="67df7c7391c2179423a95927a639492c3a177bff8f3a80e4b2d666a86e2d6f6d")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
