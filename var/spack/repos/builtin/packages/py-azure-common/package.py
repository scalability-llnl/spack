# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureCommon(PythonPackage):
    """Microsoft Azure Client Library for Python (Common)."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-common/azure-common-1.1.25.zip"

    version("1.1.25", sha256="ce0f1013e6d0e9faebaf3188cc069f4892fc60a6ec552e3f817c1a2f92835054")

    depends_on("py-setuptools", type="build")
