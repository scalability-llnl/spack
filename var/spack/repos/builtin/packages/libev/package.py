# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libev(AutotoolsPackage):
    """A full-featured and high-performance event loop that is loosely modelled
    after libevent, but without its limitations and bugs."""

    homepage = "http://software.schmorp.de/pkg/libev.html"
    url      = "http://dist.schmorp.de/libev/Attic/libev-4.24.tar.gz"
    git      = "https://github.com/enki/libev.git"

    version('develop', branch='master')
    version('4.24', sha256='973593d3479abdf657674a55afe5f78624b0e440614e2b8cb3a07f16d4d7f821')

    depends_on('autoconf', type='build', when='@develop')
    depends_on('automake', type='build', when='@develop')
    depends_on('libtool',  type='build', when='@develop')
    depends_on('m4',       type='build', when='@develop')
