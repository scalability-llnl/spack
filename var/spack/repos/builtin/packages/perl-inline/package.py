# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlInline(PerlPackage):
    """Write Perl Subroutines in Other Programming Languages"""

    homepage = "http://search.cpan.org/~ingy/Inline-0.80/lib/Inline.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/I/IN/INGY/Inline-0.80.tar.gz"

    version('0.80', sha256='7e2bd984b1ebd43e336b937896463f2c6cb682c956cbd2c311a464363d2ccef6')

    depends_on('perl-test-warn', type=('build', 'run'))
