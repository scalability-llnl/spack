# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleApiCore(PythonPackage):
    """Google API client core library."""

    homepage = "https://github.com/googleapis/python-api-core"
    pypi = "google-api-core/google-api-core-2.17.0.tar.gz"

    # 'google.api_core.operations_v1' and 'google.api_core.gapic_v1' require 'grpc'.
    # Leave them out of 'import_modules' to avoid optional dependency.
    import_modules = ["google.api_core", "google.api_core.future"]

    license("Apache-2.0")

    version("2.17.0", sha256="de7ef0450faec7c75e0aea313f29ac870fdc44cfaec9d6499a9a17305980ef66")
    version("2.16.2", sha256="032d37b45d1d6bdaf68fb11ff621e2593263a239fa9246e2e94325f9c47876d2")
    version("2.15.0", sha256="abc978a72658f14a2df1e5e12532effe40f94f868f6e23d95133bd6abcca35ca")
    version("2.14.0", sha256="5368a4502b793d9bbf812a5912e13e4e69f9bd87f6efb508460c43f5bbd1ce41")
    version("2.13.1", sha256="f2bcb43c98329f558dd13b3cd745cef04f07a107446f4f2bfc69adf09b02b994")
    version("2.12.0", sha256="c22e01b1e3c4dcd90998494879612c38d0a3411d1f7b679eb89e2abe3ce1f553")
    version("2.11.1", sha256="25d29e05a0058ed5f19c61c0a78b1b53adea4d9364b464d014fbda941f6d1c9a")
    version("2.11.0", sha256="4b9bb5d5a380a0befa0573b302651b8a9a89262c1730e37bf423cec511804c22")
    version("1.14.2", sha256="2c23fbc81c76b941ffb71301bb975ed66a610e9b03f918feacd1ed59cf43a6ec")

    variant(
        "grpc",
        default=False,
        description="Enable support for gRPC Remote Procedure Call framework.",
    )

    with when("@2:"):
        depends_on("py-setuptools", type=("build", "run"))
        depends_on("py-googleapis-common-protos@1.56.2:1", type=("build", "run"))
        depends_on("py-protobuf@3.19.5:3.19,3.20.2:4.20,4.21.6:4", type=("build", "run"))
        depends_on("py-google-auth@2.14.1:2", type=("build", "run"))
        depends_on("py-requests@2.18:2", type=("build", "run"))

        with when("+grpc"):
            depends_on("py-grpcio-status@1.49.1:1", when="^python@3.11:", type="run")
            depends_on("py-grpcio-status@1.33.2:1", when="@2.2.0:", type="run")
            depends_on("py-grpcio@1.49.1:1", when="^python@3.11:", type="run")
            depends_on("py-grpcio@1.33.2:1", type="run")

    with when("@:1"):
        depends_on("py-googleapis-common-protos@1.6:1", type=("build", "run"))
        depends_on("py-protobuf@3.4.0:", type=("build", "run"))
        depends_on("py-google-auth@0.4:1", type=("build", "run"))
        depends_on("py-requests@2.18:2", type=("build", "run"))
        depends_on("py-setuptools@34.0.0:", type=("build", "run"))
        depends_on("py-six@1.10.0:", type=("build", "run"))
        depends_on("py-pytz", type=("build", "run"))

        with when("+grpc"):
            depends_on("py-grpcio-status@1.33.2:1", when="@1.33:", type="run")
            depends_on("py-grpcio@1.33.2:1", when="@1.33:", type="run")
            depends_on("py-grpcio@1.29.0:1", when="@1.19.1", type="run")
            depends_on("py-grpcio@1.8.2:1", type="run")
