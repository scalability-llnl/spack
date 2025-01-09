# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Wget(AutotoolsPackage, GNUMirrorPackage):
    """GNU Wget is a free software package for retrieving files using
    HTTP, HTTPS and FTP, the most widely-used Internet protocols. It is a
    non-interactive commandline tool, so it may easily be called from scripts,
    cron jobs, terminals without X-Windows support, etc."""

    homepage = "https://www.gnu.org/software/wget/"
    gnu_mirror_path = "wget/wget-1.19.1.tar.gz"

    license("GPL-3.0-or-later WITH OpenSSL-Exception")

    version("1.24.5", sha256="fa2dc35bab5184ecbc46a9ef83def2aaaa3f4c9f3c97d4bd19dcb07d4da637de")
    version("1.21.4", sha256="81542f5cefb8faacc39bbbc6c82ded80e3e4a88505ae72ea51df27525bcde04c")
    version("1.21.3", sha256="5726bb8bc5ca0f6dc7110f6416e4bb7019e2d2ff5bf93d1ca2ffcc6656f220e5")
    version("1.21.2", sha256="e6d4c76be82c676dd7e8c61a29b2ac8510ae108a810b5d1d18fc9a1d2c9a2497")
    version("1.21.1", sha256="59ba0bdade9ad135eda581ae4e59a7a9f25e3a4bde6a5419632b31906120e26e")
    version("1.21", sha256="b3bc1a9bd0c19836c9709c318d41c19c11215a07514f49f89b40b9d50ab49325")
    version("1.20.3", sha256="31cccfc6630528db1c8e3a06f6decf2a370060b982841cfab2b8677400a5092e")
    version("1.19.1", sha256="9e4f12da38cc6167d0752d934abe27c7b1599a9af294e73829be7ac7b5b4da40")
    version("1.17", sha256="3e04ad027c5b6ebd67c616eec13e66fbedb3d4d8cbe19cc29dadde44b92bda55")
    version("1.16", sha256="b977fc10ac7a72d987d48136251aeb332f2dced1aabd50d6d56bdf72e2b79101")

    depends_on("c", type="build")  # generated

    variant(
        "ssl", default="openssl", values=("gnutls", "openssl"), description="Specify SSL backend"
    )
    variant("zlib", default=True, description="Enable zlib support")
    variant("libpsl", default=False, description="Enable support for libpsl cookie checking")
    variant("pcre", default=False, description="Enable PCRE style regular expressions")
    variant("python", default=False, description="Enable Python support")

    depends_on("gnutls", when="ssl=gnutls")
    depends_on("openssl", when="ssl=openssl")
    # OpenSSL 3.0 is not supported by wget, openssl@3.1: works:
    conflicts("openssl@3.0", when="ssl=openssl")

    depends_on("gettext", type="build")
    depends_on("python@3:", type="build", when="+python")

    depends_on("zlib-api", when="+zlib")
    depends_on("libpsl", when="+libpsl")
    depends_on("pcre", when="+pcre")

    depends_on("perl@5.12.0:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("iconv")

    depends_on("valgrind", type="test")

    build_directory = "spack-build"

    # gnulib bug introced in commit cbdb5ea63cb5348d9ead16dc46bedda77a4c3d7d
    # fix is from commit 84863a1c4dc8cca8fb0f6f670f67779cdd2d543b
    patch("gnulib.patch", when="@1.21.3")

    def configure_args(self):
        spec = self.spec

        args = ["--with-ssl={0}".format(spec.variants["ssl"].value), "--without-included-regex"]

        if "+zlib" in spec:
            args.append("--with-zlib")
        else:
            args.append("--without-zlib")

        if "+libpsl" in spec:
            args.append("--with-libpsl")
        else:
            args.append("--without-libpsl")

        if "+pcre" in spec:
            args.append("--enable-pcre")
        else:
            args.append("--disable-pcre")

        if self.run_tests:
            args.append("--enable-valgrind-tests")
        else:
            args.append("--disable-valgrind-tests")

        return args
