# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMinio(PythonPackage):
    """MinIO Python SDK is Simple Storage Service (aka S3) client to perform bucket
    and object operations to any Amazon S3 compatible object storage service."""

    homepage = "https://github.com/minio/minio-py"
    pypi = "minio/minio-7.1.2.tar.gz"

    license("Apache-2.0")

    version("7.1.2", sha256="40d0cdb4dba5d5610d6599ea740cf827102db5bfa71279fc220c3cf7305bedc1")

    depends_on("py-setuptools", type="build")
    depends_on("py-certifi", type=("build", "run"))
    depends_on("py-urllib3", type=("build", "run"))
