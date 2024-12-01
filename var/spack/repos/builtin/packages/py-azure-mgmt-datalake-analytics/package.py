# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtDatalakeAnalytics(PythonPackage):
    """Microsoft Azure Data Lake Analytics Management Client Library for
    Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-datalake-analytics/azure-mgmt-datalake-analytics-0.6.0.zip"

    version("0.6.0", sha256="0d64c4689a67d6138eb9ffbaff2eda2bace7d30b846401673183dcb42714de8f")
    version("0.2.1", sha256="4c7960d094f5847d9a456c18b8a3c8e60c428e3080a3905f1c943d81ba6351a4")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrestazure@0.4.27:1", when="@0.6:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.7:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
