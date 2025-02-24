# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureCore(PythonPackage):
    """Microsoft Azure Core Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/core/azure-core"
    pypi = "azure-core/azure-core-1.30.0.tar.gz"

    license("MIT")

    version("1.30.2", sha256="a14dc210efcd608821aa472d9fb8e8d035d29b68993819147bc290a8ac224472")
    version("1.30.0", sha256="6f3a7883ef184722f6bd997262eddaf80cfe7e5b3e0caaaf8db1695695893d35")
    version("1.29.7", sha256="2944faf1a7ff1558b1f457cabf60f279869cabaeef86b353bed8eb032c7d8c5e")
    version("1.29.2", sha256="beb0fe88d1043d8457318e8fb841d9caa648211092eda213c16b376401f3710d")
    version("1.28.0", sha256="e9eefc66fc1fde56dab6f04d4e5d12c60754d5a9fa49bdcfd8534fc96ed936bd")
    version("1.27.1", sha256="5975c20808fa388243f01a8b79021bfbe114f503a27c543f002c5fc8bbdd73dd")
    version("1.26.4", sha256="075fe06b74c3007950dd93d49440c2f3430fd9b4a5a2756ec8c79454afc989c6")
    version("1.26.1", sha256="223b0e90cbdd1f03c41b195b03239899843f20d00964dbb85e64386873414a2d")
    version("1.21.1", sha256="88d2db5cf9a135a7287dc45fdde6b96f9ca62c9567512a3bb3e20e322ce7deb2")
    version("1.7.0", sha256="a66da240a287f447f9867f54ba09ea235895cec13ea38c5f490ce4eedefdd75c")
    version("1.6.0", sha256="d10b74e783cff90d56360e61162afdd22276d62dc9467e657ae866449eae7648")

    # https://github.com/Azure/azure-sdk-for-python/blob/azure-core_1.30.2/sdk/core/azure-core/setup.py

    depends_on("python@3.8:", type=("build", "run"), when="@1.30.2:")
    depends_on("py-setuptools", type="build")
    depends_on("py-anyio@3:4", when="@1.29.6", type=("build", "run"))
    depends_on("py-requests@2.21:", when="@1.29.6:", type=("build", "run"))
    depends_on("py-requests@2.18.4:", type=("build", "run"))
    depends_on("py-six@1.11:", when="@1.21:", type=("build", "run"))
    depends_on("py-six@1.6:", when="@:1.21", type=("build", "run"))
    depends_on("py-typing-extensions@4.6:", when="@1.29.2:", type=("build", "run"))
    depends_on("py-typing-extensions@4.3:", when="@1.26.4:", type=("build", "run"))
    depends_on("py-typing-extensions@4.0.1:", when="@1.26:", type=("build", "run"))

    def url_for_version(self, version):
        if version < Version("1.29.3"):
            return "https://pypi.io/packages/source/a/azure-core/azure-core-{0}.zip".format(
                version
            )

        return super().url_for_version(version)
