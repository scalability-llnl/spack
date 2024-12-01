# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtEventgrid(PythonPackage):
    """Microsoft Azure EventGrid Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-eventgrid/azure-mgmt-eventgrid-2.2.0.zip"

    # Release candidate needed for py-azure-cli
    version("3.0.0rc7", sha256="68f9eb18b74fa86e07cf4e4d1a2ed16fe549bdd53f21a707b05798616b01a9d4")
    version(
        "2.2.0",
        sha256="c62058923ed20db35b04491cd1ad6a692f337244d05c377ecc14a53c06651cc3",
        preferred=True,
    )

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
