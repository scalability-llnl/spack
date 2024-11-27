# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtNspkg(PythonPackage):
    """Microsoft Azure Resource Management Namespace Package [Internal]."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-nspkg/azure-mgmt-nspkg-3.0.2.zip"

    version("3.0.2", sha256="8b2287f671529505b296005e6de9150b074344c2c7d1c805b3f053d081d58c52")

    depends_on("py-setuptools", type="build")
    depends_on("py-azure-nspkg@3.0.0:", type=("build", "run"))
