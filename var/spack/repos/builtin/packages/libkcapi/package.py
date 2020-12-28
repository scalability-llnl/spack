# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libkcapi(AutotoolsPackage):
    """libkcapi allows user-space to access the Linux kernel crypto API."""

    homepage = "https://github.com/smuellerDD/libkcapi"
    url      = "https://github.com/smuellerDD/libkcapi/archive/v1.2.0.tar.gz"

    version('1.2.0', sha256='8be75173c56342c8fe1c63a901c0d9cb750405abdc23288d04f549a960862867')
    version('1.1.5', sha256='ca38bf4d750dd2d3531ddb94d502feedb0f926bd9b29fb97e253b83bbceb6611')
    version('1.1.4', sha256='241ffa4f2813c6da442b1c1e152d489905ffab35a6c50e76aca5ee6fe60319dd')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
