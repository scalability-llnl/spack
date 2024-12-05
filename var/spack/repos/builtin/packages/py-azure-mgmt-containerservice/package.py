# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtContainerservice(PythonPackage):
    """Microsoft Azure Container Service Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-containerservice/azure-mgmt-containerservice-9.2.0.zip"

    version("9.2.0", sha256="e7904b60c42a153b64b1604f3c698602686b38787bebdaed6e808cd43b6e5967")
    version("9.0.1", sha256="7e4459679bdba4aa67a4b5848e63d94e965a304a7418ef7607eb7a9ce295d886")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
