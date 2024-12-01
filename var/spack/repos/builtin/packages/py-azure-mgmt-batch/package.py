# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtBatch(PythonPackage):
    """Microsoft Azure Batch Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-batch/azure-mgmt-batch-17.1.0.zip"

    version("17.1.0", sha256="385bf920898dc2d5807865fbe45019f10cdfbef651c6dbfa4745a842525dbafb")
    version("16.2.0", sha256="69691066cd5a2c86e8fdaaefbb80e2940381acedfc8053df193b5214d2ece682")
    version("15.0.0", sha256="9b793bb31a0d4dc8c29186db61db24d83795851a75846aadb187cf95bf853ccb")
    version("14.0.0", sha256="1d3b2c9ebd57c8874e11d29e7dd05a1f078d2156fc9683e2f2ad41024e448bf6")
    version("10.0.1", sha256="455e2f1010a59163bfd25d72e9d8dc7847df566795bc35655bcb2de925763d33")
    version("9.0.0", sha256="03417eecfa1fac906e674cb1cb43ed7da27a96277277b091d7c389ba39f6c3fe")

    # https://github.com/Azure/azure-sdk-for-python/blob/azure-mgmt-batch_14.0.0/sdk/batch/azure-mgmt-batch/setup.py

    depends_on("py-setuptools", type="build")

    depends_on("py-isodate@0.6.1:0", type=("build", "run"), when="@17.1:")
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
    depends_on("py-azure-mgmt-core@1.2:1", type=("build", "run"), when="@14:")
    depends_on("py-azure-mgmt-core@1.3:1", type=("build", "run"), when="@16.1:")
    depends_on("py-azure-mgmt-core@1.3.2:1", type=("build", "run"), when="@17:")

    with when("@:17.0"):
        depends_on("py-msrest@0.5.0:", type=("build", "run"))
        depends_on("py-msrest@0.6.21:", type=("build", "run"), when="@16:")
        depends_on("py-msrest@0.7.1:", type=("build", "run"), when="@17:")

    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"), when="@:10")
