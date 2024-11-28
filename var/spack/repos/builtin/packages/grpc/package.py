# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Grpc(CMakePackage):
    """A high performance, open-source universal RPC framework."""

    homepage = "https://grpc.io"
    url = "https://github.com/grpc/grpc/archive/v1.59.1.tar.gz"

    license("Apache-2.0 AND BSD-3-Clause AND MIT")

    version("1.66.1", sha256="79ed4ab72fa9589b20f8b0b76c16e353e4cfec1d773d33afad605d97b5682c61")
    version("1.64.0", sha256="d5509e40fb24f6390deeef8a88668124f4ec77d2ebb3b1a957b235a2f08b70c0")
    version("1.63.0", sha256="493d9905aa09124c2f44268b66205dd013f3925a7e82995f36745974e97af609")
    version("1.62.2", sha256="e5d5e0dd96fe9452fe24cc8c827381dca484c54d171fb512a198025fec81a3c8")
    version("1.61.2", sha256="86f8773434c4b8a4b64c67c91a19a90991f0da0ba054bbeb299dc1bc95fad1e9")
    version("1.59.1", sha256="916f88a34f06b56432611aaa8c55befee96d0a7b7d7457733b9deeacbc016f99")
    version("1.55.0", sha256="9cf1a69a921534ac0b760dcbefb900f3c2f735f56070bf0536506913bb5bfd74")
    version("1.50.0", sha256="76900ab068da86378395a8e125b5cc43dfae671e09ff6462ddfef18676e2165a")
    version("1.47.0", sha256="271bdc890bf329a8de5b65819f0f9590a5381402429bca37625b63546ed19e54")
    version("1.46.0", sha256="67423a4cd706ce16a88d1549297023f0f9f0d695a96dd684adc21e67b021f9bc")
    version("1.45.0", sha256="ec19657a677d49af59aa806ec299c070c882986c9fcc022b1c22c2a3caf01bcd")
    version("1.44.0", sha256="8c05641b9f91cbc92f51cc4a5b3a226788d7a63f20af4ca7aaca50d92cc94a0d")
    version("1.39.0", sha256="b16992aa1c949c10d5d5ce2a62f9d99fa7de77da2943e643fb66dcaf075826d6")
    version("1.38.1", sha256="f60e5b112913bf776a22c16a3053cc02cf55e60bf27a959fd54d7aaf8e2da6e8")
    version("1.38.0", sha256="abd9e52c69000f2c051761cfa1f12d52d8b7647b6c66828a91d462e796f2aede")
    version("1.37.1", sha256="acf247ec3a52edaee5dee28644a4e485c5e5badf46bdb24a80ca1d76cb8f1174")
    version("1.37.0", sha256="c2dc8e876ea12052d6dd16704492fd8921df8c6d38c70c4708da332cf116df22")
    version("1.36.4", sha256="8eb9d86649c4d4a7df790226df28f081b97a62bf12c5c5fe9b5d31a29cd6541a")
    version("1.36.3", sha256="bb6de0544adddd54662ba1c314eff974e84c955c39204a4a2b733ccd990354b7")
    version("1.33.1", sha256="58eaee5c0f1bd0b92ebe1fa0606ec8f14798500620e7444726afcaf65041cb63")
    version("1.32.0", sha256="f880ebeb2ccf0e47721526c10dd97469200e40b5f101a0d9774eb69efa0bd07a")
    version("1.31.0", sha256="1236514199d3deb111a6dd7f6092f67617cd2b147f7eda7adbafccea95de7381")
    version("1.30.0", sha256="419dba362eaf8f1d36849ceee17c3e2ff8ff12ac666b42d3ff02a164ebe090e9")
    version("1.29.1", sha256="0343e6dbde66e9a31c691f2f61e98d79f3584e03a11511fad3f10e3667832a45")
    version("1.29.0", sha256="c0a6b40a222e51bea5c53090e9e65de46aee2d84c7fa7638f09cb68c3331b983")
    version("1.28.2", sha256="4bec3edf82556b539f7e9f3d3801cba540e272af87293a3f4178504239bd111e")
    version("1.28.1", sha256="4cbce7f708917b6e58b631c24c59fe720acc8fef5f959df9a58cdf9558d0a79b")
    version("1.28.0", sha256="d6277f77e0bb922d3f6f56c0f93292bb4cfabfc3c92b31ee5ccea0e100303612")
    version("1.27.0", sha256="3ccc4e5ae8c1ce844456e39cc11f1c991a7da74396faabe83d779836ef449bce")
    version("1.26.0", sha256="2fcb7f1ab160d6fd3aaade64520be3e5446fc4c6fa7ba6581afdc4e26094bd81")
    version("1.25.0", sha256="ffbe61269160ea745e487f79b0fd06b6edd3d50c6d9123f053b5634737cf2f69")
    version("1.24.3", sha256="c84b3fa140fcd6cce79b3f9de6357c5733a0071e04ca4e65ba5f8d306f10f033")
    version("1.23.1", sha256="dd7da002b15641e4841f20a1f3eb1e359edb69d5ccf8ac64c362823b05f523d9")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("shared", default=False, description="Build shared instead of static libraries")
    variant(
        "codegen",
        default=True,
        description="Builds code generation plugins for protobuf " "compiler (protoc)",
    )
    variant(
        "cxxstd",
        default="11",
        values=("11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("protobuf")
    depends_on("protobuf@3.22:", when="@1.55:")
    depends_on("openssl")
    depends_on("zlib-api")
    depends_on("c-ares")

    with when("@1.27:"):
        depends_on("abseil-cpp")
        # missing includes: https://github.com/grpc/grpc/commit/bc044174401a0842b36b8682936fc93b5041cf88
        depends_on("abseil-cpp@:20230802", when="@:1.61")

    depends_on("re2+pic@2023-09-01", when="@1.33.1:")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("gRPC_BUILD_CODEGEN", "codegen"),
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            "-DgRPC_BUILD_CSHARP_EXT:Bool=OFF",
            "-DgRPC_INSTALL:Bool=ON",
            # Tell grpc to skip vendoring and look for deps via find_package:
            "-DgRPC_CARES_PROVIDER:String=package",
            "-DgRPC_ZLIB_PROVIDER:String=package",
            "-DgRPC_SSL_PROVIDER:String=package",
            "-DgRPC_PROTOBUF_PROVIDER:String=package",
            "-DgRPC_USE_PROTO_LITE:Bool=OFF",
            "-DgRPC_PROTOBUF_PACKAGE_TYPE:String=CONFIG",
            # Disable tests:
            "-DgRPC_BUILD_TESTS:BOOL=OFF",
            "-DgRPC_GFLAGS_PROVIDER:String=none",
            "-DgRPC_BENCHMARK_PROVIDER:String=none",
        ]
        if self.spec.satisfies("@1.27.0:"):
            args.append("-DgRPC_ABSL_PROVIDER:String=package")
        if self.spec.satisfies("@1.33.1:"):
            args.append("-DgRPC_RE2_PROVIDER:String=package")
        return args
