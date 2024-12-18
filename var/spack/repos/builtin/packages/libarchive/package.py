# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libarchive(AutotoolsPackage):
    """libarchive: C library and command-line tools for reading and
    writing tar, cpio, zip, ISO, and other archive formats."""

    homepage = "https://www.libarchive.org"
    url = "https://www.libarchive.org/downloads/libarchive-3.1.2.tar.gz"

    maintainers("haampie")

    license("BSD-2-Clause AND BSD-3-Clause AND Public-Domain")

    version("3.7.6", sha256="b4071807367b15b72777c2eaac80f42c8ea2d20212ab279514a19fe1f6f96ef4")
    version("3.7.5", sha256="37556113fe44d77a7988f1ef88bf86ab68f53d11e85066ffd3c70157cc5110f1")

    # Deprecated versions
    # https://nvd.nist.gov/vuln/detail/CVE-2024-48957
    version(
        "3.7.4",
        sha256="7875d49596286055b52439ed42f044bd8ad426aa4cc5aabd96bfe7abb971d5e8",
        deprecated=True,
    )
    version(
        "3.7.3",
        sha256="f27a97bc22ceb996e72502df47dc19f99f9a0f09181ae909f09f3c9eb17b67e2",
        deprecated=True,
    )
    version(
        "3.7.2",
        sha256="df404eb7222cf30b4f8f93828677890a2986b66ff8bf39dac32a804e96ddf104",
        deprecated=True,
    )
    version(
        "3.7.1",
        sha256="5d24e40819768f74daf846b99837fc53a3a9dcdf3ce1c2003fe0596db850f0f0",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="d937886a14b48c4287c4d343644feb294a14b31b7926ba9a4f1777123ce7c2cc",
        deprecated=True,
    )
    version(
        "3.6.2",
        sha256="ba6d02f15ba04aba9c23fd5f236bb234eab9d5209e95d1c4df85c44d5f19b9b3",
        deprecated=True,
    )

    # https://nvd.nist.gov/vuln/detail/CVE-2021-31566
    version(
        "3.5.2",
        sha256="5f245bd5176bc5f67428eb0aa497e09979264a153a074d35416521a5b8e86189",
        deprecated=True,
    )
    version(
        "3.5.1",
        sha256="9015d109ec00bb9ae1a384b172bf2fc1dff41e2c66e5a9eeddf933af9db37f5a",
        deprecated=True,
    )
    version(
        "3.4.1",
        sha256="fcf87f3ad8db2e4f74f32526dee62dd1fb9894782b0a503a89c9d7a70a235191",
        deprecated=True,
    )
    version(
        "3.3.2",
        sha256="ed2dbd6954792b2c054ccf8ec4b330a54b85904a80cef477a1c74643ddafa0ce",
        deprecated=True,
    )
    version(
        "3.2.1",
        sha256="72ee1a4e3fd534525f13a0ba1aa7b05b203d186e0c6072a8a4738649d0b3cfd2",
        deprecated=True,
    )
    version(
        "3.1.2",
        sha256="eb87eacd8fe49e8d90c8fdc189813023ccc319c5e752b01fb6ad0cc7b2c53d5e",
        deprecated=True,
    )
    version(
        "3.1.1",
        sha256="4968f9a3f2405ec7e07d5f6e78b36f21bceee6196df0a795165f89774bbbc6d8",
        deprecated=True,
    )
    version(
        "3.1.0",
        sha256="64b15dfa623b323da8fc9c238b5bca962ec3b38dcdfd2ed86f5f509e578a3524",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "libs",
        default="static,shared",
        values=("static", "shared"),
        multi=True,
        description="What libraries to build",
    )

    # TODO: BLAKE2 is missing
    variant(
        "compression",
        default="bz2lib,lz4,lzo2,lzma,zlib,zstd",
        values=("bz2lib", "lz4", "lzo2", "lzma", "zlib", "zstd"),
        multi=True,
        description="Supported compression",
    )
    variant(
        "xar",
        default="libxml2",
        values=("libxml2", "expat"),
        description="What library to use for xar support",
    )
    variant(
        "crypto",
        default="openssl",
        values=("mbedtls", "nettle", "openssl"),
        description="What crypto library to use for mtree and xar hashes",
    )
    variant(
        "programs",
        values=any_combination_of("bsdtar", "bsdcpio", "bsdcat"),
        description="What executables to build",
    )
    variant("iconv", default=True, description="Support iconv")

    depends_on("bzip2", when="compression=bz2lib")
    depends_on("lz4", when="compression=lz4")
    depends_on("lzo", when="compression=lzo2")
    depends_on("xz", when="compression=lzma")
    depends_on("zlib-api", when="compression=zlib")
    depends_on("zstd", when="compression=zstd")

    depends_on("nettle", when="crypto=nettle")
    depends_on("openssl", when="crypto=openssl")
    depends_on("mbedtls@2.0:2 +pic", when="crypto=mbedtls")

    depends_on("libxml2", when="xar=libxml2")
    depends_on("expat", when="xar=expat")

    depends_on("iconv", when="+iconv")

    conflicts(
        "crypto=mbedtls", when="@:3.4.1", msg="mbed TLS is only supported from libarchive 3.4.2"
    )

    # NOTE: `make check` is known to fail with the Intel compilers
    # The build test suite cannot be built with Intel

    def configure_args(self):
        spec = self.spec
        args = ["--without-libb2"]
        args += self.with_or_without("compression")
        args += self.with_or_without("crypto")
        args += self.with_or_without("xar")
        args += self.enable_or_disable("programs")

        if spec.satisfies("+iconv"):
            if spec["iconv"].name == "libiconv":
                args.append(f"--with-libiconv-prefix={spec['iconv'].prefix}")
            else:
                args.append("--without-libiconv-prefix")
        else:
            args.append("--without-iconv")

        return args
