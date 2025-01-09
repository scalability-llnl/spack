# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dcap(AutotoolsPackage):
    """dCache access protocol client library."""

    homepage = "https://github.com/dCache/dcap"
    url = "https://github.com/dCache/dcap/archive/2.47.12.tar.gz"

    license("LGPL-2.0-or-later", checked_by="wdconinc")

    version("2.47.14", sha256="dda98990d93cded815ee425101674ad2f48438fff76b3d4d5d3f91e380e9cc49")
    version("2.47.13", sha256="ae4a3845b7dd6bc32dc8ba445105e3ce72c1a25aa11da640404f63c89378876b")
    version("2.47.12", sha256="050a8d20c241abf358d5d72586f9abc43940e61d9ec9480040ac7da52ec804ac")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    variant("plugins", default=True, description="Build plugins")

    def patch(self):
        if self.spec.satisfies("~plugins"):
            filter_file("SUBDIRS = .*", "SUBDIRS = src", "Makefile.am")

    def autoreconf(self, spec, prefix):
        Executable("./bootstrap.sh")()
