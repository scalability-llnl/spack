# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libtasn1(Package):
    """ASN.1 structure parser library."""

    homepage = "https://www.gnu.org/software/libtasn1/"
    url = "https://ftp.gnu.org/gnu/libtasn1/libtasn1-4.13.tar.gz"

    license("LGPL-2.1-or-later")

    version("4.19.0", sha256="1613f0ac1cf484d6ec0ce3b8c06d56263cc7242f1c23b30d82d23de345a63f7a")
    version("4.13", sha256="7e528e8c317ddd156230c4e31d082cd13e7ddeb7a54824be82632209550c8cca")
    version("4.12", sha256="6753da2e621257f33f5b051cc114d417e5206a0818fe0b1ecfd6153f70934753")
    version("4.10", sha256="681a4d9a0d259f2125713f2e5766c5809f151b3a1392fd91390f780b4b8f5a02")
    version("4.9", sha256="4f6f7a8fd691ac2b8307c8ca365bad711db607d4ad5966f6938a9d2ecd65c920")
    version("4.8", sha256="fa802fc94d79baa00e7397cedf29eb6827d4bd8b4dd77b577373577c93a8c513")
    version("4.7", sha256="a40780dc93fc6d819170240e8ece25352058a85fd1d2347ce0f143667d8f11c9")
    version("4.6", sha256="3462fc25e2d2536878c39a8825f5e36ba2e2611b27ef535e064f4c56258e508b")
    version("4.5", sha256="89b3b5dce119273431544ecb305081f3530911001bb12e5d76588907edb71bda")
    version("4.4", sha256="f8349db1b4fe634105c77e11d26b2173e587827e86e1a489b5e38ffa822e0c5d")
    version("4.3", sha256="733513e3ffb03bd4910f97ef2683e602b40501428e4eb7649e325c2f4b1756cc")
    version("4.2", sha256="693b41cb36c2ac02d5990180b0712a79a591168e93d85f7fcbb75a0a0be4cdbb")
    version("4.1", sha256="60ee6571dcfa00cf55406404912274d6dc759cbaa80d666b89d819feeff5f301")
    version("4.0", sha256="41d044f7644bdd1c4f8a5c15ac1885ca1fcbf32f5f6dd4760a19278b979857fe")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        configure(
            "--disable-dependency-tracking",
            "--disable-silent-rules",
            "--prefix=%s" % self.spec.prefix,
        )
        make("install")
