# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrpcGoogleIamV1(PythonPackage):
    """IAM API client library."""

    homepage = "https://github.com/googleapis/python-grpc-google-iam-v1"
    pypi = "grpc_google_iam_v1/grpc-google-iam-v1-0.13.0.tar.gz"

    license("Apache-2.0")

    version("0.13.0", sha256="fad318608b9e093258fbf12529180f400d1c44453698a33509cc6ecf005b294e")

    # A workaround for invalid URL due to presence of v1 in the name.
    def url_for_version(self, version):
        return super().url_for_version(f"1-{version}")

    # https://github.com/googleapis/python-grpc-google-iam-v1/blob/v0.13.0/setup.py

    depends_on("py-grpcio@1.44:1", type=("build", "run"))
    depends_on("py-googleapis-common-protos+grpc@1.56:1", type=("build", "run"))

    depends_on("py-protobuf@3.19.5:4", type=("build", "run"))
    conflicts("py-protobuf@3.20.0,3.20.1,4.21.1:4.21.5")

    depends_on("py-setuptools", type="build")
