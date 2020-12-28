# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileListing(PerlPackage):
    """Parse directory listing"""

    homepage = "http://search.cpan.org/~gaas/File-Listing-6.04/lib/File/Listing.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/File-Listing-6.04.tar.gz"

    version('6.04', sha256='1e0050fcd6789a2179ec0db282bf1e90fb92be35d1171588bd9c47d52d959cf5')

    depends_on('perl-http-date', type=('build', 'run'))
