# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Httpd(AutotoolsPackage):
    """The Apache HTTP Server is a powerful and flexible HTTP/1.1 compliant
    web server."""

    homepage = "https://httpd.apache.org/"
    url = "https://archive.apache.org/dist/httpd/httpd-2.4.43.tar.bz2"

    license("Apache-2.0", checked_by="wdconinc")

    version("2.4.62", sha256="674188e7bf44ced82da8db522da946849e22080d73d16c93f7f4df89e25729ec")

    # https://nvd.nist.gov/vuln/detail/CVE-2024-38477
    version(
        "2.4.59",
        sha256="ec51501ec480284ff52f637258135d333230a7d229c3afa6f6c2f9040e321323",
        deprecated=True,
    )
    version(
        "2.4.55",
        sha256="11d6ba19e36c0b93ca62e47e6ffc2d2f2884942694bce0f23f39c71bdc5f69ac",
        deprecated=True,
    )

    depends_on("c", type="build")
    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("apr")
    depends_on("apr-util")
    depends_on("pcre")

    def configure_args(self):
        spec = self.spec
        config_args = [
            f"--with-apr={spec['apr'].prefix}",
            f"--with-apr-util={spec['apr-util'].prefix}",
        ]
        return config_args
