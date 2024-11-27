# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtCdn(PythonPackage):
    """Microsoft Azure CDN Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-cdn/azure-mgmt-cdn-4.0.0.zip"

    # Release candidate needed for py-azure-cli
    version("4.1.0rc1", sha256="853c73d612f5d97387e079c5841a9f1a05702173d0c7c0c59ba7b0fd86380503")
    version(
        "4.0.0",
        sha256="a53e9e09e2711ce9109329538fe9a8a1a5d0809efb231d7df481e55d09c4f02a",
        preferred=True,
    )

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
