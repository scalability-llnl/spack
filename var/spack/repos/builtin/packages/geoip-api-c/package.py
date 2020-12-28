# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GeoipApiC(AutotoolsPackage):
    """The GeoIP Legacy C library enables the user to find geographical
    and network information of an IP address."""

    homepage = "https://github.com/maxmind/geoip-api-c"
    url      = "https://github.com/maxmind/geoip-api-c/archive/v1.6.12.tar.gz"

    version('1.6.12', sha256='99b119f8e21e94f1dfd6d49fbeed29a70df1544896e76cd456f25e397b07d476')
    version('1.6.11', sha256='b0e5a92200b5ab540d118983f7b7191caf4faf1ae879c44afa3ff2a2abcdb0f5')
    version('1.6.10', sha256='cb44e0d0dbc45efe2e399e695864e58237ce00026fba8a74b31d85888c89c67a')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
