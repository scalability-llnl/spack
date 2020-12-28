# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libnet(AutotoolsPackage):
    """Libnet is an API to help with the construction and handling of
    network packets. It provides a portable framework for low-level
    network packet writing and handling """

    homepage = "https://github.com/libnet/libnet"
    url      = "https://github.com/libnet/libnet/archive/v1.2.tar.gz"

    version('1.2',     sha256='b7a371a337d242c017f3471d70bea2963596bec5bd3bd0e33e8517550e2311ef')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
