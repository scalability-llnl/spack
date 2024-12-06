# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySmartOpen(PythonPackage):
    """smart_open is a Python 2 & Python 3 library for efficient streaming of
    very large files from/to S3, HDFS, WebHDFS, HTTP, or local storage. It
    supports transparent, on-the-fly (de-)compression for a variety of
    different formats."""

    homepage = "https://github.com/piskvorky/smart_open"
    pypi = "smart_open/smart_open-5.2.1.tar.gz"
    maintainers("marcusboden")

    license("MIT")

    version("5.2.1", sha256="75abf758717a92a8f53aa96953f0c245c8cedf8e1e4184903db3659b419d4c17")
    version("1.10.0", sha256="bea5624c0c2e49987c227bdf3596573157eccd96fd1d53198856c8d53948fa2c")
    version("1.8.4", sha256="788e07f035defcbb62e3c1e313329a70b0976f4f65406ee767db73ad5d2d04f9")

    depends_on("py-setuptools", type="build")

    with when("@5:"):
        depends_on("python@3.6:3", type=("build", "run"))

        # google cloud support
        variant("gcs", default=False, description="Adds Google Cloud support")
        depends_on("py-google-cloud-storage", when="+gcs", type=("build", "run"))

        # aws support
        variant("s3", default=False, description="Adds AWS S3 support")
        depends_on("py-boto3", when="+s3", type=("build", "run"))

        # http support
        variant("http", default=True, description="Adds http and webhdfs support")
        depends_on("py-requests", when="+http", type=("build", "run"))

        # azure support
        variant("azure", default=False, description="Adds Microsoft Azure Support")
        with when("+azure"):
            depends_on("py-azure-storage-blob", type=("build", "run"))
            depends_on("py-azure-common", type=("build", "run"))
            depends_on("py-azure-core", type=("build", "run"))

    with when("@:2"):
        depends_on("py-requests", type=("build", "run"))
        depends_on("py-boto3", type=("build", "run"))
        depends_on("py-boto@2.3.2:", when="@1.8.4", type=("build", "run"))
        depends_on("py-google-cloud-storage", when="@1.10:", type=("build", "run"))
