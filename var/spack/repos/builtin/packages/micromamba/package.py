# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Micromamba(CMakePackage):
    """Mamba is a fast, robust, and cross-platform package manager (Miniconda alternative).

    Micromamba is faster and more standalone than Miniconda."""

    homepage = "https://mamba.readthedocs.io/"
    url = "https://github.com/mamba-org/mamba/archive/micromamba-1.1.0.tar.gz"

    maintainers = ["charmoniumQ"]

    version("1.1.0", sha256="e2392cd90221234ae8ea92b37f40829fbe36d80278056269aa1994a5efe7f530")

    variant(
        "linkage",
        default="dynamic",
        description="See MICROMAMBA_LINKAGE in https://mamba.readthedocs.io/en/latest/developer_zone/build_locally.html#build-micromamba",
        values=("dynamic", "static", "full_static"),
        multi=False,
    )

    with when("linkage=static"):
        # https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/CMakeLists.txt#L276
        depends_on("libarchive crypto=mbedtls xar=libxml2", type="link")
        depends_on("iconv", type="link")
        depends_on("bzip2", type="link")
        depends_on("lz4", type="link")
        depends_on("zstd", type="link")
        depends_on("zlib", type="link")
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
        depends_on("tl-expected@b74fecd", type="link")

        # https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/include/mamba/core/validate.hpp#L13
        depends_on("nlohmann-json", type="link")

        # https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/src/core/context.cpp#L7
        depends_on("cpp-termcolor", type="link")

        # https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/micromamba/src/common_options.hpp#L12
        depends_on("cli11@2.2:", type="link")

        # Experimentally, these are also required for libarchive
        depends_on("libxml2", type="link")
        depends_on("mbedtls", type="link")

    with when("linkage=full_static"):
        # See linkage=static for source
        depends_on("libarchive crypto=mbedtls xar=libxml2", type="link")
        depends_on("iconv", type="link")
        depends_on("bzip2", type="link")
        depends_on("lz4", type="link")
        depends_on("zstd", type="link")
        depends_on("zlib", type="link")
        depends_on("xz libs=static", type="link")
        depends_on("lzo", type="link")
        depends_on("libsolv+conda~shared", type="link")
        depends_on("nghttp2", type="link")
        depends_on("yaml-cpp~shared", type="link")
        depends_on("libreproc+cxx~shared", type="link")
        depends_on("fmt", type="link")
        depends_on("spdlog~shared", type="link")
        depends_on("tl-expected@b74fecd", type="link")
        depends_on("nlohmann-json", type="link")
        depends_on("cpp-termcolor", type="link")
        depends_on("cli11@2.2:", type="link")
        depends_on("libxml2", type="link")
        depends_on("mbedtls", type="link")

    with when("linkage=dynamic"):
        # See https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/CMakeLists.txt#L423
        depends_on("libsolv+conda", type=("link", "run"))
        depends_on("curl", type=("link", "run"))
        depends_on("libarchive crypto=mbedtls xar=libxml2", type=("link", "run"))
        depends_on("openssl", type=("link", "run"))
        depends_on("yaml-cpp", type=("link", "run"))
        depends_on("libreproc+cxx", type=("link", "run"))
        depends_on("tl-expected@b74fecd", type=("link", "run"))
        depends_on("fmt", type=("link", "run"))
        depends_on("spdlog", type=("link", "run"))

        # See linkage=shared for usage location
        depends_on("nlohmann-json", type="link")
        depends_on("cpp-termcolor", type="link")
        depends_on("cli11@2.2:", type="link")

    patch("fix-threads.patch")

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
            self.define("MICROMAMBA_LINKAGE", linkage.upper())
        ]

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        Executable("micromamba")("--version")
