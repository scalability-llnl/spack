# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleapisCommonProtos(PythonPackage):
    """Common protobufs used in Google APIs."""

    homepage = "https://github.com/googleapis/python-api-common-protos"
    pypi = "googleapis-common-protos/googleapis-common-protos-1.6.0.tar.gz"

    license("Apache-2.0")

    version("1.63.0", sha256="17ad01b11d5f1d0171c06d3ba5c04c54474e883b66b949722b4938ee2694ef4e")
    version("1.58.0", sha256="c727251ec025947d545184ba17e3578840fc3a24a0516a020479edab660457df")
    version("1.56.4", sha256="c25873c47279387cfdcbdafa36149887901d36202cb645a0e4f29686bf6e4417")
    version("1.55.0", sha256="53eb313064738f45d5ac634155ae208e121c963659627b90dfcb61ef514c03e1")
    version("1.6.0", sha256="e61b8ed5e36b976b487c6e7b15f31bb10c7a0ca7bd5c0e837f4afab64b53a0c6")

    # https://github.com/googleapis/python-api-common-protos/blob/v1.58.0/setup.py

    variant(
        "grpc",
        default=False,
        description="Enable support for gRPC Remote Procedure Call framework.",
    )

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        # https://github.com/googleapis/python-api-common-protos/blob/main/setup.py
        # May be able to rais max version to :5 in next release
        depends_on("py-protobuf@3.19.5:4", when="@1.58:")
        depends_on("py-protobuf@3.15.0:4", when="@1.56:1.57")
        depends_on("py-protobuf@3.12.0:4", when="@1.55")
        depends_on("py-protobuf@3.6.0:", when="@1.6.0:")

    # Explicitly incompatibile versions per setup.py
    # https://github.com/googleapis/python-api-common-protos/issues/128
    conflicts("py-protobuf@3.20:3.20.1")
    conflicts("py-protobuf@4.21.1:4.21.5")

    with when("+grpc"), default_args(type="run"):
        depends_on("py-grpcio@1.44:1", when="@1.57:")
        depends_on("py-grpcio@1:")
