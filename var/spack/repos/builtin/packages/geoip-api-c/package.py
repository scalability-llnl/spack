# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GeoipApiC(AutotoolsPackage):
    """The GeoIP Legacy C library enables the user to find geographical
    and network information of an IP address."""

    homepage = "https://github.com/maxmind/geoip-api-c"
    url = "https://github.com/maxmind/geoip-api-c/archive/v1.6.12.tar.gz"

    license("LGPL-2.1-or-later", checked_by="wdconinc")

    version("1.6.12", sha256="99b119f8e21e94f1dfd6d49fbeed29a70df1544896e76cd456f25e397b07d476")
    version("1.6.11", sha256="8859cb7c9cb63e77f4aedb40a4622024359b956b251aba46b255acbe190c34e0")
    version("1.6.10", sha256="de0d6d037d5e0ad9f7110e7f3b82eb20a24616712d29be0019e28ba7364cdc3e")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
