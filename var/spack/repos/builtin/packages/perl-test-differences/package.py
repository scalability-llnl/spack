# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestDifferences(PerlPackage):
    """Test strings and data structures and show differences if not ok"""

    homepage = "http://search.cpan.org/~dcantrell/Test-Differences-0.64/lib/Test/Differences.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DC/DCANTRELL/Test-Differences-0.64.tar.gz"

    version('0.64', sha256='9f459dd9c2302a0a73e2f5528a0ce7d09d6766f073187ae2c69e603adf2eb276')

    depends_on('perl-module-build', type='build')
    depends_on('perl-capture-tiny', type=('build', 'run'))
    depends_on('perl-text-diff', type=('build', 'run'))
