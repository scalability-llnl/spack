# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rtmpdump(MakefilePackage):
    """rtmpdump is a toolkit for RTMP streams."""

    homepage = "https://rtmpdump.mplayerhq.hu/"
    git = "https://git.ffmpeg.org/rtmpdump.git"

    maintainers("tobbez")

    license("GPL-2.0-or-later")

    version("2021-02-19", commit="f1b83c10d8beb43fcc70a6e88cf4325499f25857")

    depends_on("c", type="build")  # generated

    variant("tls", default="openssl", description="TLS backend", values=("gnutls", "openssl"))

    depends_on("openssl@:3", when="tls=openssl")
    depends_on("gnutls", when="tls=gnutls")
    depends_on("zlib-api")

    patch("missing-include.patch")
    patch("rtmpdump-fix-chunk-size.patch")
    patch("rtmpdump-openssl-1.1-v2.patch")
    patch("rtmpdump-swf_vertification_type_2.patch")
    patch("rtmpdump-swf_vertification_type_2_part_2.patch")

    @property
    def build_targets(self):
        return [f"CRYPTO={self.spec.variants['tls'].value.upper()}"]

    def install(self, spec, prefix):
        make("install", f"prefix={prefix}", "sbindir=$(bindir)")
