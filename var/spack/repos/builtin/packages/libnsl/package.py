# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libnsl(AutotoolsPackage):
    """This library contains the public client interface for NIS(YP) and NIS+
    in a IPv6 ready version."""

    homepage = "https://github.com/thkukuk/libnsl"
    url      = "https://github.com/thkukuk/libnsl/archive/v1.2.0.tar.gz"

    version('1.2.0', sha256='a5a28ef17c4ca23a005a729257c959620b09f8c7f99d0edbfe2eb6b06bafd3f8')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('pkgconfig@0.9.0:', type='build')
    depends_on('gettext')
    depends_on('rpcsvc-proto')
    depends_on('libtirpc')

    def autoreconf(self, spec, prefix):
        autoreconf = which('autoreconf')
        autoreconf('-fi')
