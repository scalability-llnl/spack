# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Weighttp(AutotoolsPackage):
    """A lightweight and simple webserver benchmarking tool"""

    homepage = "https://weighttp.lighttpd.net/"
    url = "https://github.com/lighttpd/weighttp/archive/weighttp-0.4.tar.gz"

    license("MIT")

    version("0.4", sha256="b4954f2a1eca118260ffd503a8e3504dd32942e2e61d0fa18ccb6b8166594447")
    version("0.3", sha256="376e2311af2decb8f6051e4f968d7c0ba92ca60cd563d768beb4868eb9679f45")
    version("0.2", sha256="bc2b3955126010ce27e0829285720f973df9f144e9cca2568569a657a3d5e634")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("libev")
