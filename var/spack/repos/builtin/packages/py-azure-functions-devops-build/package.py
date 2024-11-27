# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureFunctionsDevopsBuild(PythonPackage):
    """Python package for integrating Azure Functions with Azure DevOps.
    Specifically made for the Azure CLI."""

    homepage = "https://github.com/Azure/azure-functions-devops-build"
    pypi = "azure-functions-devops-build/azure-functions-devops-build-0.0.22.tar.gz"

    license("MIT")

    version("0.0.22", sha256="c6341abda6098813f8fa625acd1e925410a17a8a1c7aaabdf975bb7cecb14edf")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest", type=("build", "run"))
    depends_on("py-vsts", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
