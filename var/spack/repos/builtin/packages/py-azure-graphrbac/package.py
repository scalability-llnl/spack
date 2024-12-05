# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureGraphrbac(PythonPackage):
    """Microsoft Azure Graph RBAC Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-graphrbac/azure-graphrbac-0.61.1.zip"

    version("0.61.1", sha256="53e98ae2ca7c19b349e9e9bb1b6a824aeae8dcfcbe17190d20fe69c0f185b2e2")
    version("0.60.0", sha256="d0bb62d8bf8e196b903f3971ba4afa448e4fe14e8394ebfcdd941d84d62ecafe")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
