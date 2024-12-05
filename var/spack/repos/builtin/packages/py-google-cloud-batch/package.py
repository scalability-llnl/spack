# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudBatch(PythonPackage):
    """Google Cloud Batch API client library."""

    homepage = (
        "https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-batch"
    )

    pypi = "google-cloud-batch/google-cloud-batch-0.17.11.tar.gz"

    license("Apache-2.0")

    version("0.17.11", sha256="76e40e0605d3823965f1610210100d9c9b180cd721d11bd57782435d47769a09")

    # https://github.com/googleapis/google-cloud-python/blob/google-cloud-batch-v0.17.11/packages/google-cloud-batch/setup.py

    depends_on("py-google-api-core+grpc@1.34.0:2", type=("build", "run"))
    conflicts("py-google-api-core@2.0:2.10")

    depends_on("py-google-auth@2.14.1:2", type=("build", "run"))
    depends_on("py-proto-plus@1.22.3:1", type=("build", "run"))

    depends_on("py-protobuf@3.19.5:4", type=("build", "run"))
    conflicts("py-protobuf@3.20.0:3.20.1,4.21.0:4.21.5")

    depends_on("py-setuptools", type="build")
