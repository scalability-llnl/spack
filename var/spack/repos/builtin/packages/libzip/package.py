# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libzip(CMakePackage):
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

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        if version < Version("1.6"):
            return f"https://libzip.org/download/libzip-{version}.tar.gz"
        return f"https://github.com/nih-at/libzip/releases/download/v{version}/libzip-{version}.tar.gz"

    depends_on("zlib-api")

    variant("gnutls", default=True, description="Enable gnutls support")
    variant("bzip2", default=True, description="Enable bzip2 support")
    variant("lzma", default=True, description="Enable lzma support")
    variant("openssl", default=True, description="Enable openssl support")
    variant("zstd", default=True, description="Enable zstd support", when="@1.8:")
    variant("mbedtls", default=True, description="Enable mbedtls support")
    depends_on("gnutls", when="+gnutls")
    depends_on("bzip2", when="+bzip2")
    depends_on("lzma", when="+lzma")
    depends_on("openssl", when="+openssl")
    depends_on("mbedtls", when="+mbedtls")
    depends_on("zstd", when="+zstd")

    def cmake_args(self):
        return [
            self.define_from_variant("ENABLE_GNUTLS", "gnutls"),
            self.define_from_variant("ENABLE_MBEDTLS", "mbedtls"),
            self.define_from_variant("ENABLE_OPENSSL", "openssl"),
            self.define_from_variant("ENABLE_BZIP2", "bzip2"),
            self.define_from_variant("ENABLE_LZMA", "lzma"),
            self.define_from_variant("ENABLE_ZSTD", "zstd"),
        ]
