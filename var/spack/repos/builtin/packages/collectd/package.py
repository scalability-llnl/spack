# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Collectd(AutotoolsPackage):
    """The system statistics collection daemon."""

    homepage = "http://collectd.org/"
    url      = "https://github.com/collectd/collectd/archive/collectd-5.11.0.tar.gz"

    version('5.11.0', sha256='639676d09c5980ceea90b5a97811a9647d94e368528cce7cea3d43f0f308465d')
    version('5.10.0', sha256='bcde95a3997b5eee448d247d9414854994b3592cb9fb4fecd6ff78082cc28a1b')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
