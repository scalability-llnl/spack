# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dnsmasq(MakefilePackage):
    """A lightweight, caching DNS proxy with integrated DHCP server."""

    homepage = "https://www.thekelleys.org.uk/dnsmasq/doc.html"
    url = "http://www.thekelleys.org.uk/dnsmasq/dnsmasq-2.70.tar.gz"

    license("GPL-2.0-or-later")

    version("2.90", sha256="8f6666b542403b5ee7ccce66ea73a4a51cf19dd49392aaccd37231a2c51b303b")
    version("2.89", sha256="8651373d000cae23776256e83dcaa6723dee72c06a39362700344e0c12c4e7e4")
    version("2.81", sha256="3c28c68c6c2967c3a96e9b432c0c046a5df17a426d3a43cffe9e693cf05804d0")
    version("2.80", sha256="9e4a58f816ce0033ce383c549b7d4058ad9b823968d352d2b76614f83ea39adc")
    version("2.79", sha256="77512dd6f31ffd96718e8dcbbf54f02c083f051d4cca709bd32540aea269f789")
    version("2.78", sha256="c92e5d78aa6353354d02aabf74590d08980bb1385d8a00b80ef9bc80430aa1dc")
    version("2.77", sha256="ae97a68c4e64f07633f31249eb03190d673bdb444a05796a3a2d3f521bfe9d38")
    version("2.76", sha256="777c4762d2fee3738a0380401f2d087b47faa41db2317c60660d69ad10a76c32")
    version("2.75", sha256="f8252c0a0ba162c2cd45f81140c7c17cc40a5fca2b869d1a420835b74acad294")
    version("2.74", sha256="27b95a8b933d7eb88e93a4c405b808d09268246d4e108606e423ac518aede78f")
    version("2.73", sha256="9f350f74ae2c7990b1c7c6c8591d274c37b674aa987f54dfee7ca856fae0d02d")
    version("2.72", sha256="635f1b47417d17cf32e45cfcfd0213ac39fd09918479a25373ba9b2ce4adc05d")
    version("2.71", sha256="7d8c64f66a396442e01b639df3ea6b4e02ba88cbe206c80be8de68b6841634c4")
    version("2.70", sha256="8eb7bf53688d6aaede5c90cfd2afcce04803a4efbddfbeecc6297180749e98af")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("./src/dnsmasq", prefix.bin)
