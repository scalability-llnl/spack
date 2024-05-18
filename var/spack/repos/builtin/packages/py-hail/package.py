# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHail(MakefilePackage):
    """Cloud-native genomic dataframes and batch computing (Python API)"""

    homepage = "https://hail.is"
    git = "https://github.com/hail-is/hail.git"
    # We can't use tarballs because HAIL needs to look up git commit metadata
    # to determine its version. We could patch this, but that is not yet
    # implemented.
    #url = "https://github.com/hail-is/hail/archive/refs/tags/0.2.130.tar.gz"

    maintainers("teaguesterling")
    license("MIT", checked_by="teaguesterling")

    version(
        "0.2.130", 
        commit="bea04d9c79b5ca739364e8c121132845475f617a",
    )
    version(
        "0.2.129", 
        commit="41126be2df04e4ef823cefea40fba4cadbe5db8a",
    )

    resource(
        name="catch",
        url="https://github.com/catchorg/Catch2/releases/download/v2.6.0/catch.hpp",
        sha256="a86133b34d4721b6e1cf7171981ea469789f83f2475907b4033012577e4975fe",
        destination="hail/src/main/resources/include/catch.hpp",
        expand=False,
    )

    resource(
        name="libsimdpp-2.1",
        extension='tar.gz',
        url="https://storage.googleapis.com/hail-common/libsimdpp-2.1.tar.gz",
        sha256="b0e986b20bef77cd17004dd02db0c1ad9fab9c70d4e99594a9db1ee6a345be93",
        destination="hail/src/main/c",
    )

    variant("native", default=True)
    variant(
        "query_backend", 
        values=["undefined", "spark", "batch"], 
        default="spark"
    )

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")

    # HAIL spec, SPARK spec, SCALA spec
    bundle_versions = [("0.2", "3.3", "2.12")]
    # Hail build requirements
    with default_args(type=("build", "run")):
        depends_on("gcc@5:")
        depends_on("blas")
        depends_on("lapack")
        depends_on("lz4")
        depends_on("java@8,11")
        for hail, spark, scala in bundle_versions:
            depends_on(f"scala@{scala}", when=f"@{hail}")
            depends_on(f"spark@{spark}", when=f"@{hail}")
            # This should match spark but isn't actually enforced
            # by the PySpark package and they can conflit.
            depends_on(f"py-pyspark@{spark}", when=f"@{hail}")

    # HAIL API requirements are very specific
    with default_args(type=("build", "run")):
        depends_on("py-avro@1.10:1.11")
        depends_on("py-bokeh@:3.3")
        depends_on("py-decorator@:4.4.2")
        depends_on("py-deprecated@1.2.10:1.2")
        depends_on("py-numpy@:2")
        depends_on("py-pandas@2")
        depends_on("py-parsimonious@:0")
        depends_on("py-plotly@5.18:5.20")
        depends_on("py-protobuf@3.20.2")
        depends_on("py-requests@2.31")
        depends_on("py-scipy@1.3:1.11")

    # HAIL wheels are pinned to a specific version of
    # Spark. If we implement building from source, this
    # will likely not be as much of an issue, but that
    # isn't working yet.
    #with default_args(type=("build", "run")):
    #    depends_on("py-pyspark@3.3", when="@0.2.130")


    # hailtop requirements
    with default_args(type=("build", "run")):
        depends_on("py-aiodns@2")
        depends_on("py-aiohttp@3.9")
        depends_on("py-azure-identity@1.6:1")
        depends_on("py-azure-mgmt-storage@20.1.0")
        depends_on("py-azure-storage-blob@12.11:12")
        depends_on("py-boto3@1.17:1")
        depends_on("py-botocore@1.20:1")
        depends_on("py-dill@0.3.6:0.3")
        depends_on("py-frozenlist@1.3.1:1")
        depends_on("py-google-auth@2.14.1:2")
        depends_on("py-google-auth-oauthlib@0.5.2:0")
        depends_on("py-humanize@1.0.0:1")
        depends_on("py-janus@0.6:1.0")
        depends_on("py-nest-asyncio@1.5.8:1")
        depends_on("py-rich@12.6.0:12")
        depends_on("py-orjson@3.9.15:3")
        depends_on("py-typer@0.9.0:0")
        depends_on("py-python-json-logger@2.0.2:2")
        depends_on("py-pyyaml@6.0:7")
        depends_on("py-sortedcontainers@2.4.0:2")
        depends_on("py-tabulate@0.8.9:0")
        depends_on("py-uvloop@0.19.0:0")
        depends_on("py-jproperties@2.1.1:2")
        # Undocumented runtime requirements for hailtop
        # These are also required to use the HAIL API
        # but are not explicitly mentioned anywhere
        depends_on("py-azure-mgmt-core")
        depends_on("py-typing-extensions")


    patch("fix-lz4-import-builtins.patch")

    build_directory = "hail"

    @property
    def hail_pip_version(self):
        # This is the same behavior is as is defined in hail/version.mk
        return f"{self.spec.version.up_to(3)}"

    @property
    def build_wheel_file_path(self):
        wheel_file = f"hail-{self.hail_pip_version}-py3-none-any.whl"
        wheel_dir = join_path("build", "deploy", "dist")
        return join_path(wheel_dir, wheel_file)

    def setup_build_environment(self, env):
        # HAIL build doesn't find lz4: https://discuss.hail.is/t/ld-pruning-repeated-errors/1838/14
        env.append_flags("CXXFLAGS", f"-I{self.spec['lz4'].prefix.include}")

    @property
    def build_targets(self):
        spec = self.spec
        variables = [
            f"SCALA_VERSION={spec['scala'].version}",
            f"SPARK_VERSION={spec['spark'].version}",
        ]
        if spec.satisfies("+native"):
            variables += ["HAIL_COMPILE_NATIVES=1"]

        # We're not using the documented target to 
        # because it depends on pipto install and resolve 
        # dependencies directly and does everythin in one step.
        # The documented target is `install-on-cluster`
        targets = [
            # This may be too specific but it would detect failures
            # and fail to build instead of taking a long time to build
            # and then failing at install time.
            self.build_wheel_file_path,
        ]

        return targets + variables

    def install(self, spec, prefix):
        spec = self.spec
        python = which("pip")
        wheel = self.build_wheel_file_path

        # This mimics the install-on-cluster target but avoids anything
        # that utilizes pip to resolve dependencies
        with working_dir(join_path(self.stage.source_path, "hail")):
            pip("install", "--use-pep517", "--no-deps", f"--prefix={prefix}", wheel)

        backend = spec.variants['query_backend'].value
        if backend != "undefined":
            hailctl = which("hailctl")  # Should be installed from above
            if hailctl is not None:  # but it might not be
                hailctl("config", "set", "query/backend", f"{backend}")

    def setup_run_environment(self, env):
        #TODO: Add Spark configuration values to find HAIL Jars
        #This would be needed if one was connecting to a Spark
        #cluster that was started outside of HAIL
        pass
