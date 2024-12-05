# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyS3fs(PythonPackage):
    """S3FS builds on aiobotocore to provide a convenient Python filesystem
    interface for S3."""

    homepage = "https://s3fs.readthedocs.io/en/latest/"
    pypi = "s3fs/s3fs-0.5.2.tar.gz"

    license("BSD-3-Clause")

    version("2024.2.0", sha256="f8064f522ad088b56b043047c825734847c0269df19f2613c956d4c20de15b62")
    version("2022.11.0", sha256="10c5ac283a4f5b67ffad6d1f25ff7ee026142750c5c5dc868746cd904f617c33")
    version("0.5.2", sha256="87e5210415db17b9de18c77bcfc4a301570cc9030ee112b77dc47ab82426bae1")

    depends_on("py-setuptools", type="build")
    depends_on("py-aiobotocore@2.5.4:2", when="@2024:", type=("build", "run"))
    depends_on("py-aiobotocore@2.4", when="@2022", type=("build", "run"))
    depends_on("py-aiobotocore@1.0.1:", when="@:0", type=("build", "run"))
    depends_on("py-fsspec@2024.2.0", when="@2024.2.0", type=("build", "run"))
    depends_on("py-fsspec@2022.11.0", when="@2022.11.0", type=("build", "run"))
    depends_on("py-fsspec@0.8.0:", when="@0", type=("build", "run"))
    depends_on("py-aiohttp", when="@2022:", type=("build", "run"))
