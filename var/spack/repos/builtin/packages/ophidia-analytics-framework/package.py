# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OphidiaAnalyticsFramework(AutotoolsPackage):
    """Core modules and operators of the Ophidia framework"""

    homepage = "https://github.com/OphidiaBigData/ophidia-analytics-framework"
    url = "https://github.com/OphidiaBigData/ophidia-analytics-framework/archive/refs/tags/v1.7.3.tar.gz"
    maintainers("eldoo", "SoniaScard")
    version("1.7.3", sha256="f8fc6374613efd10d9878e216b40494fd38622389c52005e3b85dd9956fa7cd5")
    version(
        "1.7.1",
        sha256="565050b90ce1cefc59136c835a335ca7981fec792df7a1ee9309b24c05b275d6",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("gsl")
    depends_on("mpich")
    depends_on("jansson")
    depends_on("libxml2")
    depends_on("libssh2")
    depends_on("openssl")
    depends_on("mysql")
    depends_on("netcdf-c")
    depends_on("curl")
    depends_on("ophidia-io-server")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = [
            "--enable-parallel-netcdf",
            "--with-web-server-path={0}/html".format(
                self.spec["ophidia-analytics-framework"].prefix
            ),
            "--with-web-server-url=http://127.0.0.1/ophidia",
            "--with-ophidiaio-server-path={0}".format(self.spec["ophidia-io-server"].prefix),
        ]
        return args
