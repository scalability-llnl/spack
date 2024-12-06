# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureLoganalytics(PythonPackage):
    """Microsoft Azure Log Analytics Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-loganalytics/azure-loganalytics-0.1.0.zip"

    version("0.1.0", sha256="3ceb350def677a351f34b0a0d1637df6be0c6fe87ff32a5270b17f540f6da06e")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.4.29:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
