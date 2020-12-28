# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nmap(AutotoolsPackage):
    """Nmap ("Network Mapper") is a free and open source (license)
       utility for network discovery and security auditing.
       It also provides ncat an updated nc"""

    homepage = "https://nmap.org"
    url      = "https://nmap.org/dist/nmap-7.70.tar.bz2"

    version('7.70', sha256='847b068955f792f4cc247593aca6dc3dc4aae12976169873247488de147a6e18')
    version('7.31', sha256='cb9f4e03c0771c709cd47dc8fc6ac3421eadbdd313f0aae52276829290583842')
    version('7.30', sha256='ba38a042ec67e315d903d28a4976b74999da94c646667c0c63f31e587d6d8d0f')
