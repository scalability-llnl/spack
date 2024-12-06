# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtSearch(PythonPackage):
    """Microsoft Azure Search Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-search/azure-mgmt-search-2.1.0.zip"

    version("2.1.0", sha256="92a40a1a7a9e3a82b6fa302042799e8d5a67d3996c20835af72afc14f1610501")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
