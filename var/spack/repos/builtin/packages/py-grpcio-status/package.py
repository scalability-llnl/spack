# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrpcioStatus(PythonPackage):
    """Status proto mapping for gRPC."""

    homepage = "https://grpc.io/"
    pypi = "grpcio_status/grpcio-status-1.60.1.tar.gz"

    license("Apache-2.0")

    # Versions 1.63.0 and 1.64.0 are released but not yet on pypi

    version("1.62.2", sha256="62e1bfcb02025a1cd73732a2d33672d3e9d0df4d21c12c51e0bbcaf09bab742a")
    version("1.60.1", sha256="61b5aab8989498e8aa142c20b88829ea5d90d18c18c853b9f9e6d407d37bf8b4")
    version("1.56.2", sha256="a046b2c0118df4a5687f4585cca9d3c3bae5c498c4dff055dcb43fb06a1180c8")

    # https://github.com/grpc/grpc/blob/v1.60.1/src/python/grpcio_status/setup.py

    with default_args(type=("build", "run")):
        depends_on("py-protobuf@4.21.6:")
        for grpcio in ("1.62.2", "1.60.1", "1.56.2"):
            depends_on(f"py-grpcio@{grpcio}", when=f"@{grpcio}")
        depends_on("py-googleapis-common-protos@1.5.5:")

    depends_on("py-setuptools", type="build")
