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
    # url = "https://github.com/hail-is/hail/archive/refs/tags/0.2.130.tar.gz"

    maintainers("teaguesterling")
    license("MIT", checked_by="teaguesterling")

    version("0.2.132", commit="678e1f52b9999cb05ebf03fd360e5c4506bd6dad")
    version("0.2.131", commit="11d9b2ff89da9ef6a4f576be89f1f06959580ea4")
    version("0.2.130", commit="bea04d9c79b5ca739364e8c121132845475f617a")
    version("0.2.129", commit="41126be2df04e4ef823cefea40fba4cadbe5db8a")

    resource(
        name="catch",
        url="https://github.com/catchorg/Catch2/releases/download/v2.6.0/catch.hpp",
        sha256="a86133b34d4721b6e1cf7171981ea469789f83f2475907b4033012577e4975fe",
        destination="hail/src/main/resources/include/catch.hpp",
        expand=False,
    )

    resource(
        name="libsimdpp-2.1",
        extension="tar.gz",
        url="https://storage.googleapis.com/hail-common/libsimdpp-2.1.tar.gz",
        sha256="b0e986b20bef77cd17004dd02db0c1ad9fab9c70d4e99594a9db1ee6a345be93",
        destination="hail/src/main/c",
    )

    resource(
        name="mill-0.11.7",
        url="https://repo1.maven.org/maven2/com/lihaoyi/mill-dist/0.11.7/mill-dist-0.11.7.jar",
        sha256="278b430150af899495d360d1f886e223e78bb4a20e67144a240bfb7e2d4f6085",
        destination="hail/mill",
        expand=False,
    )

    variant("native", default=True, description="Compile C & C++ HAIL optimizations")
    variant(
        "query_backend",
        values=["undefined", "spark", "batch"],
        default="spark",
        description="Configure HAIL query backend at build",
    )

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-build@1.1+virtualenv", type="build", when="@0.2.131:")
    depends_on("c", type="build", when="+native")
    depends_on("cxx", type="build", when="+native")

    # HAIL bundle is tied to specific runtime versions
    # HAIL spec, Java sec, Spark spec, Scala spec
    # We're not accurately capturing previous versions
    for hail, java, spark, scala in [
        # 0.2.130 and before (to somwhere around 0.2.64) used Spark 3.3
        # And either Java 8 or Java 11
        (":0.2.130", "8,11", "3.3", "2.12"),
        # 0.2.131 updated to Java 11 and Spark 3.5
        # Undocumented bump was to scala 2.12.13 for scala.annotation.noerror
        ("0.2.131:", "11", "3.5", "2.12.18:2.12"),
    ]:
        with default_args(type=("build", "run"), when=f"@{hail}"):
            depends_on(f"java@{java}")
            depends_on(f"scala@{scala}")
            depends_on(f"spark@{spark}")
            # This should match spark but isn't actually enforced
            # by the PySpark package and they can conflit.
            depends_on(f"py-pyspark@{spark}")

    with default_args(type=("build", "link"), when="+native"):
        # Hail build requirements
        depends_on("blas")
        depends_on("lapack")
        depends_on("lz4")

    with default_args(type=("build", "run")):
        depends_on("py-avro@1.10:1.11")
        depends_on("py-bokeh@3:3.3")
        depends_on("py-decorator@:4")
        depends_on("py-deprecated@1.2.10:1.2")
        depends_on("py-numpy@:1")
        depends_on("py-pandas@2:2")
        depends_on("py-parsimonious@:0")
        depends_on("py-plotly@5.18:5")
        depends_on("py-protobuf@3.20.2")
        depends_on("py-requests@2.31:2")
        depends_on("py-scipy@1.3:1.11")

        # hailtop requirements
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

    build_directory = "hail"

    def patch(self):
        # Hail will fail to build if it cannot determine a commit hash from git
        # which will not be available in a spack cache. Since we know it from
        # the package, we can inject it in the failure and move forward.
        revision = self.hail_revision
        version = self.hail_pip_version

        filter_file(
            r'\$\(error "git rev-parse HEAD" failed to produce output\)',
            f"REVISION := {revision}",
            "hail/version.mk",
        )
        filter_file(
            r'\$\(error "git rev-parse --short=12 HEAD" failed to produce output\)',
            f"SHORT_REVISION := {revision[:12]}",
            "hail/version.mk",
        )
        filter_file(
            r'\$\(error "git rev-parse --abbrev-ref HEAD" failed to produce output\)',
            f"BRANCH := tags/{version}",
            "hail/version.mk",
        )

        # Also need to make sure that build-info.properties gets the right revision
        # which ends up improperly calculated in scala and will crash at runtime
        filter_file(
            r"val revision = VcsVersion\.vcsState\(\)\.currentRevision",
            "val vcs_revision = VcsVersion.vcsState().currentRevision\n"
            f'  val revision = if(vcs_revision ==  "no-vcs") "{revision}" else vcs_revision\n',
            "hail/build.sc",
        )

    @property
    def hail_revision(self):
        version = self.version
        version_info = self.versions[version]
        # REVISION must look like a hash or Hail crashes at startup
        # Technically, it needs to be at least 12 characters
        revision = version_info.get("commit", version.joined.string.ljust(40, "0"))
        return revision

    @property
    def hail_pip_version(self):
        # This is the same behavior is as is defined in hail/version.mk
        return f"{self.spec.version.up_to(3)}"

    @property
    def build_wheel_file_path(self):
        wheel_file = f"hail-{self.hail_pip_version}-py3-none-any.whl"
        wheel_dir = join_path("build", "deploy", "dist")
        return join_path(wheel_dir, wheel_file)

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.satisfies("+native"):
            # HAIL build doesn't find lz4: https://discuss.hail.is/t/ld-pruning-repeated-errors/1838/14
            flags.append(f"-I{self.spec['lz4'].prefix.include}")
        return (flags, None, None)

    @property
    def build_targets(self):
        spec = self.spec

        # Hail likes variables passed in to Make
        variables = [
            f"HAIL_PYTHON3={spec['python'].home.bin.python3}",
            f"PIP={spec['py-pip'].home.bin.pip}",
            f"SCALA_VERSION={spec['scala'].version}",
            f"SPARK_VERSION={spec['spark'].version}",
        ]
        if spec.satisfies("+native"):
            variables += ["HAIL_COMPILE_NATIVES=1"]

        # We're not using the documented target to
        # because it depends on pip to install and resolve
        # dependencies directly. This does everything in one step.
        # and ends up downloading all of the dependencies via pip.
        # The documented target is `install-on-cluster`
        targets = [
            # This may be too specific but it would detect failures
            # and fail to build instead of taking a long time to build
            # and then failing at install time.
            self.build_wheel_file_path
        ]

        return targets + variables

    def install(self, spec, prefix):
        spec = self.spec
        pip = which("pip")
        wheel = self.build_wheel_file_path

        # This mimics the install-on-cluster target but avoids anything
        # that utilizes pip to resolve dependencies
        with working_dir(join_path(self.stage.source_path, "hail")):
            pip("install", "--use-pep517", "--no-deps", f"--prefix={prefix}", wheel)

        backend = spec.variants["query_backend"].value
        if backend != "undefined":
            hailctl = which("hailctl")  # Should be installed from above
            if hailctl is not None:  # but it might not be
                hailctl("config", "set", "query/backend", f"{backend}")
