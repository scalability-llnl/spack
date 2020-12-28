# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxcrypt(AutotoolsPackage):
    """libxcrypt is a modern library for one-way hashing of passwords."""

    homepage = "https://github.com/besser82/libxcrypt"
    url      = "https://github.com/besser82/libxcrypt/archive/v4.4.17.tar.gz"

    version('4.4.17', sha256='7665168d0409574a03f7b484682e68334764c29c21ca5df438955a381384ca07')
    version('4.4.16', sha256='a98f65b8baffa2b5ba68ee53c10c0a328166ef4116bce3baece190c8ce01f375')
    version('4.4.15', sha256='8bcdef03bc65f9dbda742e56820435b6f13eea59fb903765141c6467f4655e5a')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
