# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureStorageNspkg(PythonPackage):
    """Microsoft Azure Storage Namespace Package."""

    homepage = "https://github.com/Azure/azure-storage-python"
    pypi = "azure-storage-nspkg/azure-storage-nspkg-3.1.0.tar.gz"

    version("3.1.0", sha256="6f3bbe8652d5f542767d8433e7f96b8df7f518774055ac7c92ed7ca85f653811")

    depends_on("py-setuptools", type="build")
    depends_on("py-azure-nspkg@2.0.0:", type=("build", "run"))
