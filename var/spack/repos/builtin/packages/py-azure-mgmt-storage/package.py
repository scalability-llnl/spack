# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtStorage(PythonPackage):
    """Microsoft Azure Storage Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-storage/azure-mgmt-storage-11.1.0.zip"

    version("21.0.0", sha256="6eb13eeecf89195b2b5f47be0679e3f27888efd7bd2132eec7ebcbce75cb1377")
    version("20.1.0", sha256="214f3fde8c91e27d53f2e654a28d15003ad3f6f15c8438a8205f0c88a48d9451")
    version("11.1.0", sha256="ef23587c1b6dc0866ebf0e91e83ba05d7f7e4fea7951b704781b9cd9f5f27f1c")
    version("11.0.0", sha256="f9791c2a84eee0a55bbf757632a2a4d1e102db958e75422d5e0e7306041129b8")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
