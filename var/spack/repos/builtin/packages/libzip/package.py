# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.build_systems.autotools
import spack.build_systems.cmake
from spack.package import *


class Libzip(CMakePackage, AutotoolsPackage):
    """libzip is a C library for reading, creating,
    and modifying zip archives."""

    homepage = "https://libzip.org/"
    maintainers("prudhomm")
    license("BSD-3-Clause")

    # current versions are released on GitHub
    version("1.11.1", sha256="c0e6fa52a62ba11efd30262290dc6970947aef32e0cc294ee50e9005ceac092a")
    version("1.10.1", sha256="9669ae5dfe3ac5b3897536dc8466a874c8cf2c0e3b1fdd08d75b273884299363")
    version("1.9.2", sha256="fd6a7f745de3d69cf5603edc9cb33d2890f0198e415255d0987a0cf10d824c6f")
    version("1.8.0", sha256="30ee55868c0a698d3c600492f2bea4eb62c53849bcf696d21af5eb65f3f3839e")
    version("1.7.3", sha256="0e2276c550c5a310d4ebf3a2c3dfc43fb3b4602a072ff625842ad4f3238cb9cc")
    version(
        "1.6.1",
        sha256="06eb8e9141fd19e2788cabaea9c9c2fd4d488d9e1484eb474bbfcac78e7b1d88",
        url="https://github.com/nih-at/libzip/releases/download/rel-1-6-1/libzip-1.6.1.tar.gz",
    )
    # older releases are available on libzip.org
    version(
        "1.3.2",
        sha256="ab4c34eb6c3a08b678cd0f2450a6c57a13e9618b1ba34ee45d00eb5327316457",
        deprecated=True,
    )
    version(
        "1.2.0",
        sha256="6cf9840e427db96ebf3936665430bab204c9ebbd0120c326459077ed9c907d9f",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        if version < Version("1.6"):
            return f"https://libzip.org/download/libzip-{version}.tar.gz"
        return f"https://github.com/nih-at/libzip/releases/download/v{version}/libzip-{version}.tar.gz"

    depends_on("zlib-api")

    # Build system
    build_system(
        conditional("cmake", when="@1.4:"), conditional("autotools", when="@:1.3"), default="cmake"
    )

    # Required dependencies
    with when("build_system=cmake"):
        variant("gnutls", default=True, description="Enable gnutls support")
        variant("bzip2", default=True, description="Enable bzip2 support")
        variant("lzma", default=True, description="Enable lzma support")
        variant("openssl", default=True, description="Enable openssl support")
        variant("zstd", default=True, description="Enable zstd support")
        variant("mbedtls", default=True, description="Enable mbedtls support")
        depends_on("gnutls", when="+gnutls")
        depends_on("bzip2", when="+bzip2")
        depends_on("lzma", when="+lzma")
        depends_on("openssl", when="+openssl")
        depends_on("zstd", when="+zstd")
        depends_on("mbedtls", when="+mbedtls")

    @property
    def headers(self):
        # Up to version 1.3.0 zipconf.h was installed outside of self.prefix.include
        return find_all_headers(
            self.prefix if self.spec.satisfies("@:1.3.0") else self.prefix.include
        )


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        return [
            self.define_from_variant("ENABLE_GNUTLS", "gnutls"),
            self.define_from_variant("ENABLE_MBEDTLS", "mbedtls"),
            self.define_from_variant("ENABLE_OPENSSL", "openssl"),
            self.define_from_variant("ENABLE_BZIP2", "bz2"),
            self.define_from_variant("ENABLE_LZMA", "lzma"),
            self.define_from_variant("ENABLE_ZSTD", "zstd"),
        ]
