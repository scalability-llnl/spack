# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtPolicyinsights(PythonPackage):
    """Microsoft Azure Policy Insights Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-policyinsights/azure-mgmt-policyinsights-0.5.0.zip"

    version("0.5.0", sha256="ed229e3845c477e88dde413825d4fba0d38b3a5ffab4e694c7d0da995f3db0f3")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
