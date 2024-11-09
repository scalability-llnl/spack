# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class LibjpegTurbo(CMakePackage, AutotoolsPackage):
    """libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to
    accelerate baseline JPEG compression and decompression.

    libjpeg is a library that implements JPEG image encoding, decoding and
    transcoding.
    """

    maintainers("AlexanderRichert-NOAA")

    # https://github.com/libjpeg-turbo/libjpeg-turbo/blob/master/BUILDING.md
    homepage = "https://libjpeg-turbo.org/"
    url = "https://github.com/libjpeg-turbo/libjpeg-turbo/archive/2.0.3.tar.gz"

    license("BSD-3-Clause AND IJG AND Zlib")

    version("3.0.3", sha256="a649205a90e39a548863a3614a9576a3fb4465f8e8e66d54999f127957c25b21")
    version("3.0.2", sha256="29f2197345aafe1dcaadc8b055e4cbec9f35aad2a318d61ea081f835af2eebe9")
    version("3.0.1", sha256="5b9bbca2b2a87c6632c821799438d358e27004ab528abf798533c15d50b39f82")
    version("3.0.0", sha256="171dae5d73560bc94006a7c0c3281bd9bfde6a34f7e41e66f930a1a9162bd7df")
    version("2.1.5.1", sha256="61846251941e5791005fb7face196eec24541fce04f12570c308557529e92c75")
    version("2.1.5", sha256="254f3642b04e309fee775123133c6464181addc150499561020312ec61c1bf7c")
    version("2.1.4", sha256="a78b05c0d8427a90eb5b4eb08af25309770c8379592bb0b8a863373128e6143f")
    version("2.1.3", sha256="dbda0c685942aa3ea908496592491e5ec8160d2cf1ec9d5fd5470e50768e7859")
    version("2.1.2", sha256="e7fdc8a255c45bc8fbd9aa11c1a49c23092fcd7379296aeaeb14d3343a3d1bed")
    version("2.1.1", sha256="20e9cd3e5f517950dfb7a300ad344543d88719c254407ffb5ad88d891bf701c4")
    version("2.1.0", sha256="d6b7790927d658108dfd3bee2f0c66a2924c51ee7f9dc930f62c452f4a638c52")
    version("2.0.6", sha256="005aee2fcdca252cee42271f7f90574dda64ca6505d9f8b86ae61abc2b426371")
    version("2.0.5", sha256="b3090cd37b5a8b3e4dbd30a1311b3989a894e5d3c668f14cbc6739d77c9402b7")
    version("2.0.4", sha256="7777c3c19762940cff42b3ba4d7cd5c52d1671b39a79532050c85efb99079064")
    version("2.0.3", sha256="a69598bf079463b34d45ca7268462a18b6507fdaa62bb1dfd212f02041499b5d")
    version("2.0.2", sha256="b45255bd476c19c7c6b198c07c0487e8b8536373b82f2b38346b32b4fa7bb942")
    version("1.5.90", sha256="cb948ade92561d8626fd7866a4a7ba3b952f9759ea3dd642927bc687470f60b7")
    version(
        "1.5.3",
        sha256="1a17020f859cb12711175a67eab5c71fc1904e04b587046218e36106e07eabde",
        deprecated=True,
    )
    version(
        "1.5.0",
        sha256="232280e1c9c3e6a1de95fe99be2f7f9c0362ee08f3e3e48d50ee83b9a2ed955b",
        deprecated=True,
    )
    version(
        "1.3.1",
        sha256="5008aeeac303ea9159a0ec3ccff295434f4e63b05aed4a684c9964d497304524",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    provides("jpeg")

    build_system(
        conditional("autotools", when="@:1.5.3"),
        conditional("cmake", when="@1.5.90:"),
        default="cmake",
    )

    variant(
        "libs",
        default=("shared", "static"),
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs, or both",
    )
    variant("jpeg8", default=False, description="Emulate libjpeg v8 API/ABI")
    variant(
        "pic", default=True, description="Enable position independent code", when="libs=static"
    )
    variant(
        "partial_decoder",
        default=False,
        description="add partial_decode_scale functionality required for rocAL",
    )

    patch(
        "https://github.com/libjpeg-turbo/libjpeg-turbo/commit/09c71da06a6346dca132db66f26f959f7e4dd5ad.patch?full_index=1",
        sha256="4d5bdfb5de5b04399144254ea383f5357ab7beb830b398aeb35b65f21dd6b4b0",
        when="@2.0.6 +partial_decoder",
    )
    patch(
        "https://github.com/libjpeg-turbo/libjpeg-turbo/commit/640d7ee1917fcd3b6a5271aa6cf4576bccc7c5fb.patch?full_index=1",
        sha256="dc1ec567c2356b652100ecdc28713bbf25f544e46f7d2947f31a2395c362cc48",
        when="@2.0.6 +partial_decoder",
    )

    # Can use either of these. But in the current version of the package
    # only nasm is used. In order to use yasm an environmental variable
    # NASM must be set.
    # TODO: Implement the selection between two supported assemblers.
    # depends_on('yasm', type='build')
    depends_on("nasm", type="build")
    with when("build_system=autotools"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")

    with when("build_system=cmake"):
        depends_on("cmake", type="build", when="@1.5.90:")

    @property
    def libs(self):
        shared = self.spec.satisfies("libs=shared")
        name = "jpeg" if sys.platform == "win32" else "libjpeg*"
        return find_libraries(name, root=self.prefix, shared=shared, recursive=True, runtime=False)


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        args = [
            self.define("ENABLE_SHARED", self.spec.satisfies("libs=shared")),
            self.define("ENABLE_STATIC", self.spec.satisfies("libs=static")),
            self.define_from_variant("WITH_JPEG8", "jpeg8"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
        ]

        return args

    @run_after("install")
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies("platform=darwin") and self.spec.satisfies("+shared"):
            fix_darwin_install_name(self.prefix.lib)
