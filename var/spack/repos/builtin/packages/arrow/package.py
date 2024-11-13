# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Arrow(CMakePackage, CudaPackage):
    """A cross-language development platform for in-memory data.

    This package contains the C++ bindings.
    """

    homepage = "https://arrow.apache.org"
    url = "https://github.com/apache/arrow/archive/apache-arrow-0.9.0.tar.gz"

    license("Apache-2.0")

    version("16.1.0", sha256="9762d9ecc13d09de2a03f9c625a74db0d645cb012de1e9a10dfed0b4ddc09524")
    version("15.0.2", sha256="4735b349845bff1fe95ed11abbfed204eb092cabc37523aa13a80cb830fe5b5e")
    version("14.0.2", sha256="07cdb4da6795487c800526b2865c150ab7d80b8512a31793e6a7147c8ccd270f")
    version("14.0.1", sha256="a48e54a09d58168bc04d86b13e7dab04f0aaba18a6f7e4dadf3e9c7bb835c8f1")
    version("14.0.0", sha256="39e3388bbaba23faa7a5e8a82ebba7fe4c38ace2c394d6a3f26559715b30f401")
    version("13.0.0", sha256="99c27e6a517c750f29c3e6b264836e31251bb8e978dbbf11316680ca3eb8ebda")
    version("12.0.1", sha256="f01b76a42ceb30409e7b1953ef64379297dd0c08502547cae6aaafd2c4a4d92e")
    version("12.0.0", sha256="f25901c486e1e79cde8b78b3e7b1d889919f942549996003a7341a8ee86addaa")
    version("11.0.0", sha256="4a8c0c3d5b39ca81f4a636a41863f1cf5e0ed199f994bf5ead0854ca037eb741")
    version("10.0.1", sha256="28c3e0402bc1c3c1e047b6e26cedb8d1d89b2b9497d576af24b0b700eef11701")
    version("9.0.0", sha256="bb187b4b0af8dcc027fffed3700a7b891c9f76c9b63ad8925b4afb8257a2bb1b")
    version("8.0.0", sha256="19ece12de48e51ce4287d2dee00dc358fbc5ff02f41629d16076f77b8579e272")
    version("7.0.0", sha256="57e13c62f27b710e1de54fd30faed612aefa22aa41fa2c0c3bacd204dd18a8f3")
    version("4.0.1", sha256="79d3e807df4a179cfab1e7a1ab5f79d95f7b72ac2c33aba030febd125d77eb3b")
    version("3.0.0", sha256="fc461c4f0a60e7470a7c58b28e9344aa8fb0be5cc982e9658970217e084c3a82")
    version("0.17.1", sha256="ecb6da20f9288c0ca31f9b457ffdd460198765a8af27c1cac4b1382a8d130f86")
    version("0.15.1", sha256="ab1c0d371a10b615eccfcead71bb79832245d788f4834cc6b278c03c3872d593")
    version("0.15.0", sha256="d1072d8c4bf9166949f4b722a89350a88b7c8912f51642a5d52283448acdfd58")
    version("0.14.1", sha256="69d9de9ec60a3080543b28a5334dbaf892ca34235b8bd8f8c1c01a33253926c1")
    version("0.12.1", sha256="aae68622edc3dcadaa16b2d25ae3f00290d5233100321993427b03bcf5b1dd3b")
    version("0.11.0", sha256="0ac629a7775d86108e403eb66d9f1a3d3bdd6b3a497a86228aa4e8143364b7cc")
    version("0.9.0", sha256="65f89a3910b6df02ac71e4d4283db9b02c5b3f1e627346c7b6a5982ae994af91")
    version("0.8.0", sha256="c61a60c298c30546fc0b418a35be66ef330fb81b06c49928acca7f1a34671d54")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("boost@1.60: +filesystem +system")
    depends_on("brotli", when="+brotli")
    depends_on("bzip2", when="+bz2")
    depends_on("cmake@3.2.0:", type="build")
    depends_on("flatbuffers")
    conflicts("%gcc@14", when="@:15.0.1")  # https://github.com/apache/arrow/issues/40009
    depends_on("llvm@:11 +clang", when="+gandiva @:3", type="build")
    depends_on("llvm@:12 +clang", when="+gandiva @:4", type="build")
    depends_on("llvm@:13 +clang", when="+gandiva @:7", type="build")
    depends_on("llvm@:14 +clang", when="+gandiva @8:", type="build")
    depends_on("lz4", when="+lz4")
    depends_on("ninja", type="build")
    depends_on("openssl", when="+gandiva @6.0.0:")
    depends_on("openssl", when="@4.0.0:")
    depends_on("orc", when="+orc")
    depends_on("protobuf", when="+gandiva")
    depends_on("py-numpy", when="+python")
    depends_on("python", when="+python")
    depends_on("rapidjson")
    depends_on("re2+shared", when="+compute")
    depends_on("re2+shared", when="+gandiva")
    depends_on("re2+shared", when="+python")
    depends_on("snappy~shared", when="+snappy @9:")
    depends_on("snappy~shared", when="@8:")
    depends_on("thrift+pic", when="+parquet")
    depends_on("utf8proc@2.7.0: +shared", when="+compute")
    depends_on("utf8proc@2.7.0: +shared", when="+gandiva")
    depends_on("utf8proc@2.7.0: +shared", when="+python")
    depends_on("xsimd@8.1.0:", when="@9.0.0:")
    depends_on("zlib-api", when="+zlib @9:")
    depends_on("zlib-api", when="@:8")
    conflicts("^zlib~pic")
    depends_on("zstd", when="+zstd @9:")
    depends_on("zstd", when="@:8")

    variant("brotli", default=False, description="Build support for Brotli compression")
    variant("bz2", default=False, description="Build support for bzip2 compression")
    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "FastDebug", "Release"),
    )
    variant(
        "compute", default=False, description="Computational kernel functions and other support"
    )
    variant("gandiva", default=False, description="Build Gandiva support")
    variant(
        "glog",
        default=False,
        description="Build libraries with glog support for pluggable logging",
    )
    variant(
        "hdfs",
        default=False,
        description="Integration with libhdfs for accessing the Hadoop Filesystem",
    )
    variant("ipc", default=True, description="Build the Arrow IPC extensions")
    variant("jemalloc", default=False, description="Build the Arrow jemalloc-based allocator")
    variant("lz4", default=False, description="Build support for lz4 compression")
    variant("orc", default=False, description="Build integration with Apache ORC")
    variant("parquet", default=False, description="Build Parquet interface")
    variant("python", default=False, description="Build Python interface")
    variant("shared", default=True, description="Build shared libs")
    variant("snappy", default=False, description="Build support for Snappy compression")
    variant("tensorflow", default=False, description="Build Arrow with TensorFlow support enabled")
    variant("zlib", default=False, description="Build support for zlib (gzip) compression")
    variant("zstd", default=False, description="Build support for ZSTD compression")

    root_cmakelists_dir = "cpp"

    def patch(self):
        """Prevent `-isystem /usr/include` from appearing, since this confuses gcc."""
        filter_file(
            r"(include_directories\()SYSTEM ", r"\1", "cpp/cmake_modules/ThirdpartyToolchain.cmake"
        )

        if self.spec.satisfies("@:2.0.0"):
            filter_file(
                r'set\(ARROW_LLVM_VERSIONS "10" "9" "8" "7"\)',
                'set(ARROW_LLVM_VERSIONS "11" "10" "9" "8" "7")',
                "cpp/CMakeLists.txt",
            )
            filter_file(
                r"#include <llvm/Support/DynamicLibrary\.h>",
                r"#include <llvm/Support/DynamicLibrary.h>"
                + "\n"
                + r"#include <llvm/Support/Host.h>",
                "cpp/src/gandiva/engine.cc",
            )

    def cmake_args(self):
        args = ["-DARROW_DEPENDENCY_SOURCE=SYSTEM", "-DARROW_NO_DEPRECATED_API=ON"]

        if self.spec.satisfies("+shared"):
            args.append(self.define("BUILD_SHARED", "ON"))
        else:
            args.append(self.define("BUILD_SHARED", "OFF"))
            args.append(self.define("BUILD_STATIC", "ON"))

        if self.spec.satisfies("@:0.11.99"):
            # ARROW_USE_SSE was removed in 0.12
            # see https://issues.apache.org/jira/browse/ARROW-3844
            args.append(self.define("ARROW_USE_SSE", "ON"))

        args.append(self.define_from_variant("ARROW_COMPUTE", "compute"))
        args.append(self.define_from_variant("ARROW_CUDA", "cuda"))
        args.append(self.define_from_variant("ARROW_GANDIVA", "gandiva"))
        args.append(self.define_from_variant("ARROW_GLOG", "glog"))
        args.append(self.define_from_variant("ARROW_HDFS", "hdfs"))
        args.append(self.define_from_variant("ARROW_IPC", "ipc"))
        args.append(self.define_from_variant("ARROW_JEMALLOC", "jemalloc"))
        args.append(self.define_from_variant("ARROW_ORC", "orc"))
        args.append(self.define_from_variant("ARROW_PARQUET", "parquet"))
        args.append(self.define_from_variant("ARROW_PYTHON", "python"))
        args.append(self.define_from_variant("ARROW_TENSORFLOW", "tensorflow"))
        args.append(self.define_from_variant("ARROW_WITH_BROTLI", "brotli"))
        args.append(self.define_from_variant("ARROW_WITH_BZ2", "bz2"))
        args.append(self.define_from_variant("ARROW_WITH_LZ4", "lz4"))
        args.append(self.define_from_variant("ARROW_WITH_SNAPPY", "snappy"))
        args.append(self.define_from_variant("ARROW_WITH_ZLIB", "zlib"))
        args.append(self.define_from_variant("ARROW_WITH_ZSTD", "zstd"))

        if not self.spec.dependencies("re2"):
            args.append(self.define("ARROW_WITH_RE2", False))
        if not self.spec.dependencies("utf8proc"):
            args.append(self.define("ARROW_WITH_UTF8PROC", False))

        if self.spec.satisfies("@:8"):
            args.extend(
                [
                    self.define("FLATBUFFERS_HOME", self.spec["flatbuffers"].prefix),
                    self.define("RAPIDJSON_HOME", self.spec["rapidjson"].prefix),
                    self.define("ZSTD_HOME", self.spec["zstd"].prefix),
                    self.define("ZLIB_HOME", self.spec["zlib-api"].prefix),
                    self.define("ZLIB_LIBRARIES", self.spec["zlib-api"].libs),
                ]
            )

            if self.spec.satisfies("+snappy"):
                args.append(self.define("SNAPPY_HOME", self.spec["snappy"].prefix))

        return args
