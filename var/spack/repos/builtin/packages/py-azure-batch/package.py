# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureBatch(PythonPackage):
    """Microsoft Azure Batch Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-batch/azure-batch-14.2.0.tar.gz"

    version("14.2.0", sha256="c79267d6c3d3fe14a16a422ab5bbfabcbd68ed0b58b6bbcdfa0c8345c4c78532")
    version("14.0.0", sha256="165b1e99b86f821024c4fae85fb34869d407aa0ebb0ca4b96fb26d859c26c934")
    version("13.0.0", sha256="e9295de70404d276eda0dd2253d76397439abe5d8f18c1fca199c49b8d6ae30a")
    version("12.0.0", sha256="1a9b1e178984a7bf495af67bcce51f0db1e4a8a957afb29e33554a14a9674deb")
    version("11.0.0", sha256="ce5fdb0ec962eddfe85cd82205e9177cb0bbdb445265746e38b3bbbf1f16dc73")
    version("10.0.0", sha256="83d7a2b0be42ca456ac2b56fa3dc6ce704c130e888d37d924072c1d3718f32d0")
    version("9.0.0", sha256="47ca6f50a640915e1cdc5ce3c1307abe5fa3a636236e561119cf62d9df384d84")

    # https://github.com/Azure/azure-sdk-for-python/blob/azure-batch_14.2.0/sdk/batch/azure-batch/setup.py

    depends_on("py-setuptools", type="build")

    depends_on("py-msrestazure@0.4.32:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))

    with when("@:12"):
        depends_on("py-msrest@0.6.21:", when="@11:", type=("build", "run"))
        depends_on("py-msrest@0.5.0:", type=("build", "run"))

    def url_for_version(self, version):
        if version < Version("14.1.0"):
            return "https://pypi.io/packages/source/a/azure-batch/azure-batch-{0}.zip".format(
                version
            )

        return super().url_for_version(version)
