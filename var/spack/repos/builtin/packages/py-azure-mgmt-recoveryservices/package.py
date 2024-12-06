# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtRecoveryservices(PythonPackage):
    """Microsoft Azure Recovery Services Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-recoveryservices/azure-mgmt-recoveryservices-0.5.0.zip"

    version("0.5.0", sha256="3c90e6b2e358dbe6d5c6d7204955bdf52c3e977c6f8b727cbbb8811427d7fd52")
    version("0.4.0", sha256="e1e794760232239f8a9328d5de1740565ff70d1612a2921c9609746ba5671e6c")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
