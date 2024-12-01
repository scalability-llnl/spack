# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

linkage_url = (
    "https://mamba.readthedocs.io/en/latest/developer_zone/build_locally.html#build-micromamba"
)


class Micromamba(CMakePackage):
    """Mamba is a fast, robust, and cross-platform package manager (Miniconda alternative).

    Micromamba is faster than Miniconda, and it is a standalone
    executable, whereas Miniconda pulls in its own Python environment.

    """

    homepage = "https://mamba.readthedocs.io/"
    url = "https://github.com/mamba-org/mamba/archive/micromamba-1.1.0.tar.gz"

    maintainers("charmoniumQ")

    license("BSD-3-Clause")

    version("1.4.2", sha256="dce034908d02d991c5e9aadeb9d01f139d027ba199aaeb1d47d543e3f24895d1")
    version("1.1.0", sha256="e2392cd90221234ae8ea92b37f40829fbe36d80278056269aa1994a5efe7f530")

    depends_on("cxx", type="build")  # generated

    variant(
        "linkage",
        default="dynamic",
        description=f"See MICROMAMBA_LINKAGE in {linkage_url}.",
        values=("dynamic", conditional("static", when="@1.1.0")),
        multi=False,
    )

    patch("fix-threads.patch")

    with when("linkage=dynamic"):
        # See https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/CMakeLists.txt#L423
        depends_on("libsolv+conda", type="link")
        depends_on("curl libs=shared", type="link")
        depends_on("libarchive crypto=mbedtls xar=libxml2", type="link")
        depends_on("openssl", type="link")
        depends_on("yaml-cpp", type="link")
        depends_on("libreproc+cxx+shared", type="link")
        depends_on("tl-expected@2022-11-24", type="link")
        depends_on("fmt@9.1.0", type="link")
        depends_on("spdlog@1.11.0", type="link")

        # https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/include/mamba/core/validate.hpp#L13
        depends_on("nlohmann-json", type="link")

        # https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/src/core/context.cpp#L7
        depends_on("cpp-termcolor", type="link")

        # https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/micromamba/src/common_options.hpp#L12
        depends_on("cli11@2.2:", type="link")

        depends_on("zstd build_system=cmake", type="link", when="@1.4.0:")

        # 1.4.2 made the static build the old "full_static" build and it needs some work.
    with when("linkage=static"):
        # When linkage is static, BUILD_STATIC=ON
        # and then
        # https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/CMakeLists.txt#L523
        # calls libmamba_create_target(libmamba-static STATIC SHARED libmamba)
        # where the third argument, SHARED, is the deps_linkage
        # as defined here,
        # https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/CMakeLists.txt#L256
        # which would use dynamic linkage here,
        # https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/CMakeLists.txt#L420
        # See linkage=dynamic for what that entails.
        depends_on("libsolv+conda", type="link")
        depends_on("curl libs=shared", type="link")
        depends_on("libarchive crypto=mbedtls xar=libxml2", type="link")
        depends_on("openssl", type="link")
        depends_on("yaml-cpp", type="link")
        depends_on("libreproc+cxx", type="link")
        depends_on("tl-expected@2022-11-24", type="link")
        depends_on("fmt@9.1.0", type="link")
        depends_on("spdlog@1.11.0", type="link")
        depends_on("nlohmann-json", type="link")
        depends_on("cpp-termcolor", type="link")
        depends_on("cli11@2.2:", type="link")

    if False:
        # This variant currently fails with:
        #
        #     libarchive/archive_digest.c:191: undefined reference to `mbedtls_sha512_free'
        #
        # These shouldn't be necessary,
        # since they are already in 'libarchive crypto=mbedtls xar=libxml2'
        # but even adding them doesn't fix it.
        #
        #     depends_on("libxml2", type="link")
        #     depends_on("mbedtls", type="link")
        #
        # However, I wanted to live this variant in the code,
        # so it serves as a starting point.

        with when("linkage=full_static"):
            # https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/CMakeLists.txt#L276
            depends_on("curl libs=static", type="link")
            depends_on("libssh2~shared", type="link")
            depends_on("krb5~shared", type="link")
            depends_on("openssl~shared", type="link")
            depends_on("libarchive crypto=mbedtls xar=libxml2", type="link")
            depends_on("iconv", type="link")
            depends_on("bzip2", type="link")
            depends_on("lz4", type="link")
            depends_on("zstd", type="link")
            depends_on("zlib-api", type="link")
            depends_on("xz libs=static", type="link")
            depends_on("lzo", type="link")
            depends_on("libsolv+conda~shared", type="link")
            depends_on("nghttp2", type="link")
            depends_on("yaml-cpp~shared", type="link")
            depends_on("libreproc+cxx~shared", type="link")

            # https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/CMakeLists.txt#L342
            depends_on("fmt", type="link")
            depends_on("spdlog~shared", type="link")

            # https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/include/mamba/core/error_handling.hpp#L9
            depends_on("tl-expected@2022-11-24", type="link")

            # See linkage=dynamic for usage location
            depends_on("nlohmann-json", type="link")
            depends_on("cpp-termcolor", type="link")
            depends_on("cli11@2.2:", type="link")

    def cmake_args(self):
        # See https://mamba.readthedocs.io/en/latest/developer_zone/build_locally.html#build-micromamba
        if "linkage=dynamic" in self.spec:
            linkage = "dynamic"
        elif "linkage=static" in self.spec:
            linkage = "static"
        elif "linkage=full_static" in self.spec:
            linkage = "full_static"
        else:
            raise ValueError(f"Unknown linkage type {self.spec}")
        return [
            self.define("BUILD_LIBMAMBA", True),
            self.define("BUILD_MICROMAMBA", True),
            self.define("BUILD_STATIC", linkage == "static"),
            self.define("BUILD_STATIC_DEPS", linkage == "full_static"),
            self.define("BUILD_SHARED", linkage == "dynamic"),
            self.define("MICROMAMBA_LINKAGE", linkage.upper()),
        ]

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        Executable("micromamba")("--version")
