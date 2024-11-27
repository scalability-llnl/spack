# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dropwatch(AutotoolsPackage):
    """Dropwatch is a project I started in an effort to improve the
    ability for developers and system administrator to diagnose problems
    in the Linux Networking stack, specifically in our ability to
    diagnose where packets are getting dropped."""

    homepage = "https://github.com/nhorman/dropwatch"
    url = "https://github.com/nhorman/dropwatch/archive/v1.5.3.tar.gz"

    license("GPL-2.0")

    version("1.5.4", sha256="8c43d0c15d0cb9ce179fa1fb0610611723689a6f551b23c70a7ddc1cf068e8d2")
    version("1.5.3", sha256="b748b66a816c1f94531446c0451da5461a4a31b0949244bb867d741c6ac0148b")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("libnl")
    depends_on("libpcap")
    depends_on("binutils")
    depends_on("readline")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def check(self):
        """`make check` starts a daemon which does not terminate, blocking the builds"""
        pass
