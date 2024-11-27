# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyspark(PythonPackage):
    """Python bindings for Apache Spark"""

    homepage = "https://spark.apache.org"
    pypi = "pyspark/pyspark-3.0.1.tar.gz"

    maintainers("teaguesterling")

    version("3.5.1", sha256="dd6569e547365eadc4f887bf57f153e4d582a68c4b490de475d55b9981664910")
    version("3.4.3", sha256="8d7025fa274830cb6c3bd592228be3d9345cb3b8b1e324018c2aa6e75f48a208")
    version("3.3.4", sha256="1f866be47130a522355240949ed50d9812a8f327bd7619f043ffe07fbcf7f7b6")
    version("3.3.1", sha256="e99fa7de92be406884bfd831c32b9306a3a99de44cfc39a2eefb6ed07445d5fa")
    version("3.3.0", sha256="7ebe8e9505647b4d124d5a82fca60dfd3891021cf8ad6c5ec88777eeece92cf7")
    version("3.2.1", sha256="0b81359262ec6e9ac78c353344e7de026027d140c6def949ff0d80ab70f89a54")
    version("3.1.3", sha256="39ac641ef5559a3d1286154779fc990316e9934520853615ae4785c1af52d14b")
    version("3.1.2", sha256="5e25ebb18756e9715f4d26848cc7e558035025da74b4fc325a0ebc05ff538e65")
    version("3.0.1", sha256="38b485d3634a86c9a2923c39c8f08f003fdd0e0a3d7f07114b2fb4392ce60479")

    variant("java", default=True, description="Include Java requirements via py-py4j")
    variant("pandas", default=True, description="Include Pandas support")
    variant("connect", default=True, description="Include SparkConnect support", when="@3.4:")

    # Noted on https://spark.apache.org/docs/latest/api/python/getting_started/install.html#dependencies
    with default_args(type="run"):
        depends_on("py-pyarrow@4:", when="+pandas@3.5:")
        depends_on("py-pyarrow@1:", when="+pandas@:3.4")
        depends_on("py-pandas@1.0.5:", when="+pandas")
        depends_on("py-numpy@1.15:", when="+pandas")

        with when("@3.5:"):
            depends_on("py-grpcio@1.56:", when="+connect")
            depends_on("py-grpcio-status@1.56:", when="+connect")
            depends_on("py-googleapis-common-protos@1.56.4:", when="+connect")

        with when("@3.4:"):
            depends_on("py-grpcio@1.48.1:", when="+connect")
            depends_on("py-grpcio-status@1.48.1:", when="+connect")
            depends_on("py-googleapis-common-protos@1.56.4:", when="+connect")

    depends_on("py-setuptools", type="build")
    with default_args(type=("build", "run")):
        depends_on("py-py4j~java", when="~java")
        for py4j_version, pyspark_version in [
            ("0.10.9.7", "3.4:"),
            ("0.10.9.5", "3.3:"),
            ("0.10.9.3", "3.2.1"),
            ("0.10.9", "3.0.1:3.1.3"),
        ]:
            depends_on(f"py-py4j@{py4j_version}:", when=f"@{pyspark_version}")

    def setup_run_environment(self, env):
        env.set("PYSPARK_PYTHON", python.path)
        env.set("PYSPARK_DRIVER_PYTHON", python.path)
        if self.spec.satisfies("+pandas ^java@11:"):
            env.append_flags("SPARK_SUBMIT_OPTS", "-Dio.netty.tryReflectionSetAccessible=true")
