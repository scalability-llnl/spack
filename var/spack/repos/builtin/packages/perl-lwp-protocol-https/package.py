# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLwpProtocolHttps(PerlPackage):
    """ Provide https support for LWP::UserAgent"""

    homepage = "http://search.cpan.org/~gaas/LWP-Protocol-https-6.04/lib/LWP/Protocol/https.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/LWP-Protocol-https-6.04.tar.gz"

    version('6.04', sha256='1ef67750ee363525cf729b59afde805ac4dc80eaf8d36ca01082a4d78a7af629')

    depends_on('perl-test-requiresinternet', type=('build', 'run'))
    depends_on('perl-io-socket-ssl', type=('build', 'run'))
    depends_on('perl-net-http', type=('build', 'run'))
    depends_on('perl-mozilla-ca', type=('build', 'run'))
    depends_on('perl-libwww-perl', type=('build', 'run'))
