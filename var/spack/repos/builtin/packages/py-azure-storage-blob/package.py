# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureStorageBlob(PythonPackage):
    """Microsoft Azure Blob Storage Client Library for Python"""

    homepage = "https://github.com/Azure/azure-storage-python"
    pypi = "azure-storage-blob/azure-storage-blob-12.19.0.tar.gz"
    maintainers("marcusboden")

    license("MIT")

    version("12.22.0", sha256="b3804bb4fe8ab1c32771fa464053da772a682c2737b19da438a3f4e5e3b3736e")
    version("12.19.0", sha256="26c0a4320a34a3c2a1b74528ba6812ebcb632a04cd67b1c7377232c4b01a5897")
    version("12.18.3", sha256="d8ced0deee3367fa3d4f3d1a03cd9edadf4440c0a371f503d623fa6c807554ee")
    version("12.17.0", sha256="c14b785a17050b30fc326a315bdae6bc4a078855f4f94a4c303ad74a48dc8c63")
    version("12.16.0", sha256="43b45f19a518a5c6895632f263b3825ebc23574f25cc84b66e1630a6160e466f")
    version("12.15.0", sha256="f8b8d582492740ab16744455408342fb8e4c8897b64a8a3fc31743844722c2f2")
    version("12.14.0", sha256="a72dd9923e4b38a552f2bc1749d1fa5b820f497a8fb3cd2d77e7045bbe87bb4d")
    version("12.13.1", sha256="899c4b8e2671812d2cf78f107556a27dbb128caaa2bb06094e72a3d5836740af")
    version("12.12.0", sha256="f6daf07d1ca86d189ae15c9b1859dff5b7127bf24a07a4bbe41e0b81e01d62f7")
    version("12.11.0", sha256="49535b3190bb69d0d9ff7a383246b14da4d2b1bdff60cae5f9173920c67ca7ee")
    version("12.10.0", sha256="3c7dc2c93e7ff2a731acd66a36a1f0a6266072b4154deba4894dab891285ea3a")
    version("12.9.0", sha256="cff66a115c73c90e496c8c8b3026898a3ce64100840276e9245434e28a864225")

    # https://github.com/Azure/azure-sdk-for-python/blob/azure-storage-blob_12.22.0/sdk/storage/azure-storage-blob/setup.py

    depends_on("python@3.8:", type=("build", "run"), when="@12.20:")
    depends_on("py-setuptools", type="build")
    depends_on("py-azure-core@1.28:", type=("build", "run"), when="@12.20:")
    depends_on("py-azure-core@1.28:1", type=("build", "run"), when="@12.17:12.19")
    depends_on("py-azure-core@1.26:1", type=("build", "run"), when="@12.15:12.16")
    depends_on("py-azure-core@1.24.2:1", type=("build", "run"), when="@12.14")
    depends_on("py-azure-core@1.23.1:1", type=("build", "run"), when="@12.12:12.13")
    depends_on("py-azure-core@1.15:1", type=("build", "run"), when="@12.10:12.11")
    depends_on("py-azure-core@1.10:1", type=("build", "run"), when="@:12.19")
    depends_on("py-cryptography@2.1.4:", type=("build", "run"))
    depends_on("py-typing-extensions@4.6:", type=("build", "run"), when="@12.20:")
    depends_on("py-typing-extensions@4.3:", type=("build", "run"), when="@12.17:")
    depends_on("py-typing-extensions@4.0.1:", type=("build", "run"), when="@12.15:")
    depends_on("py-isodate@0.6.1:", type=("build", "run"), when="@12.15:")
    depends_on("py-msrest@0.7.1:", type=("build", "run"), when="@12.14")
    depends_on("py-msrest@0.6.21:", type=("build", "run"), when="@:12.13")

    def url_for_version(self, version):
        if version < Version("12.18"):
            return "https://pypi.io/packages/source/a/azure-storage-blob/azure-storage-blob-{0}.zip".format(
                version
            )

        return super().url_for_version(version)
