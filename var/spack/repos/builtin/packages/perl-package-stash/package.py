# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPackageStash(PerlPackage):
    """Routines for manipulating stashes"""

    homepage = "http://search.cpan.org/~doy/Package-Stash-0.37/lib/Package/Stash.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Package-Stash-0.37.tar.gz"

    version('0.37', sha256='06ab05388f9130cd377c0e1d3e3bafeed6ef6a1e22104571a9e1d7bfac787b2c')

    depends_on('perl-test-requires', type=('build', 'run'))
    depends_on('perl-test-fatal', type=('build', 'run'))
    depends_on('perl-module-implementation', type=('build', 'run'))
    depends_on('perl-dist-checkconflicts', type=('build', 'run'))
