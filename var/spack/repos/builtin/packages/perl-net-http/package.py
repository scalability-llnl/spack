# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNetHttp(PerlPackage):
    """Low-level HTTP connection (client)"""

    homepage = "http://search.cpan.org/~oalders/Net-HTTP-6.17/lib/Net/HTTP.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/Net-HTTP-6.17.tar.gz"

    version('6.17', sha256='1e8624b1618dc6f7f605f5545643ebb9b833930f4d7485d4124aa2f2f26d1611')

    depends_on('perl-uri', type=('build', 'run'))
