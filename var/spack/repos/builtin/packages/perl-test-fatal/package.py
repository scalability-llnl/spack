# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestFatal(PerlPackage):
    """Incredibly simple helpers for testing code with exceptions"""

    homepage = "http://search.cpan.org/~rjbs/Test-Fatal-0.014/lib/Test/Fatal.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Test-Fatal-0.014.tar.gz"

    version('0.014', sha256='bcdcef5c7b2790a187ebca810b0a08221a63256062cfab3c3b98685d91d1cbb0')

    depends_on('perl-try-tiny', type=('build', 'run'))
