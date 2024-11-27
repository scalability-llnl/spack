# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtRecoveryservicesbackup(PythonPackage):
    """Microsoft Azure Recovery Services Backup Management Client Library for
    Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-recoveryservicesbackup/azure-mgmt-recoveryservicesbackup-0.8.0.zip"

    version("0.8.0", sha256="a0ee89691b21945cc4b892a9194320f50c1cd242d98f00a82d7e3848c28517a5")
    version("0.6.0", sha256="4df62479c90a6f93e7689f9d58e0a139899f0407f5e3298d5ce014442599428f")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
