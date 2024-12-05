# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtContainerregistry(PythonPackage):
    """Microsoft Azure Container Registry Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-containerregistry/azure-mgmt-containerregistry-2.8.0.zip"

    # Release candidate needed for py-azure-cli
    version("3.0.0rc14", sha256="d23ce93ec5903d00f79f0ac995e16bf47197130239f7f182509add3277b73071")
    version(
        "2.8.0",
        sha256="b24be1050d54f3158e8be7f6ad677f0c8888dddefd09fb8391ebfc73d40173a4",
        preferred=True,
    )

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
