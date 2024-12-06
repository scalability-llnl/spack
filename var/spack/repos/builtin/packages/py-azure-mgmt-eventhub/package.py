# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtEventhub(PythonPackage):
    """Microsoft Azure EventHub Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-eventhub/azure-mgmt-eventhub-4.0.0.zip"

    version("4.0.0", sha256="65223196cf132899656c2f9cb71a14c972d99e5ecd815ee050dae1072cb73ae2")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
