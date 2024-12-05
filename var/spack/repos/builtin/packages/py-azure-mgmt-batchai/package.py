# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtBatchai(PythonPackage):
    """Microsoft Azure Batch AI Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-batchai/azure-mgmt-batchai-2.0.0.zip"

    version("2.0.0", sha256="f1870b0f97d5001cdb66208e5a236c9717a0ed18b34dbfdb238a828f3ca2a683")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrestazure@0.4.20:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
