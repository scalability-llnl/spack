# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureDatalakeStore(PythonPackage):
    """Azure Data Lake Store Filesystem Client Library for Python."""

    homepage = "https://github.com/Azure/azure-data-lake-store-python"
    pypi = "azure-datalake-store/azure-datalake-store-0.0.48.tar.gz"

    version("0.0.48", sha256="d27c335783d4add00b3a5f709341e4a8009857440209e15a739a9a96b52386f7")

    depends_on("py-setuptools", type="build")
    depends_on("py-cffi", type=("build", "run"))
    depends_on("py-adal@0.4.2:", type=("build", "run"))
    depends_on("py-requests@2.20.0:", type=("build", "run"))
