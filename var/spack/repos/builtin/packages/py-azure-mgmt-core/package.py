# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtCore(PythonPackage):
    """Microsoft Azure Management Core Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/core/azure-mgmt-core"
    pypi = "azure-mgmt-core/azure-mgmt-core-1.2.0.zip"

    license("MIT")

    version("1.4.0", sha256="d195208340094f98e5a6661b781cde6f6a051e79ce317caabd8ff97030a9b3ae")
    version("1.3.2", sha256="07f4afe823a55d704b048d61edfdc1318c051ed59f244032126350be95e9d501")
    version("1.2.2", sha256="4246810996107f72482a9351cf918d380c257e90942144ec9c0c2abda1d0a312")
    version("1.2.0", sha256="8fe3b59446438f27e34f7b24ea692a982034d9e734617ca1320eedeee1939998")
    version("1.0.0", sha256="510faf49a10daec8346cc086143d8e667ef3b4f8c8022a8e710091027631a55e")

    # https://github.com/Azure/azure-sdk-for-python/blob/azure-mgmt-core_1.4.0/sdk/core/azure-mgmt-core/setup.py

    depends_on("py-setuptools", type="build")
    depends_on("py-azure-core@1.26.2:1", when="@1.4.0:", type=("build", "run"))
    depends_on("py-azure-core@1.24:1", when="@1.3.2:", type=("build", "run"))
    depends_on("py-azure-core@1.23:1", when="@1.3.1:", type=("build", "run"))
    depends_on("py-azure-core@1.15:1", when="@1.3:", type=("build", "run"))
    depends_on("py-azure-core@1.9:1", when="@1.2.2:", type=("build", "run"))
    depends_on("py-azure-core@1.8.2:1", when="@1.2.1:", type=("build", "run"))
    depends_on("py-azure-core@1.7.0:1", when="@1.2:", type=("build", "run"))
    depends_on("py-azure-core@1.4.0:1", type=("build", "run"))
