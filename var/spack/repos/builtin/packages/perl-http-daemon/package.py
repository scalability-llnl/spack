# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpDaemon(PerlPackage):
    """A simple http server class"""

    homepage = "http://search.cpan.org/~gaas/HTTP-Daemon-6.01/lib/HTTP/Daemon.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/HTTP-Daemon-6.01.tar.gz"

    version('6.01', sha256='43fd867742701a3f9fcc7bd59838ab72c6490c0ebaf66901068ec6997514adc2')

    depends_on('perl-lwp-mediatypes', type=('build', 'run'))
    depends_on('perl-http-message', type=('build', 'run'))
    depends_on('perl-http-date', type=('build', 'run'))
    depends_on('perl-module-build-tiny', type='build')
