# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OphidiaServer(AutotoolsPackage):
    """Front-end server of the Ophidia framework"""

    homepage = "https://github.com/OphidiaBigData/ophidia-server"
    url = "https://github.com/OphidiaBigData/ophidia-server/archive/refs/tags/v1.7.4.tar.gz"
    maintainers("eldoo", "SoniaScard")
    version("1.7.4", sha256="30128c99ae089ab766141397ea5098ac930cfe10d09b289ed120f6581d8bb07d")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("libmatheval")
    depends_on("jansson")
    depends_on("libxml2")
    depends_on("libssh2")
    depends_on("openssl")
    depends_on("mysql")
    depends_on("curl")
    depends_on("ophidia-analytics-framework")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = [
            "--with-web-server-path={0}/html".format(
                self.spec["ophidia-analytics-framework"].prefix
            ),
            "--with-web-server-url=http://127.0.0.1/ophidia",
            "--with-framework-path={0}".format(self.spec["ophidia-analytics-framework"].prefix),
        ]

        return args
