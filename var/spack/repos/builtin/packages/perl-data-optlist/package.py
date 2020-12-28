# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDataOptlist(PerlPackage):
    """Parse and validate simple name/value option pairs"""

    homepage = "http://search.cpan.org/~rjbs/Data-OptList-0.110/lib/Data/OptList.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Data-OptList-0.110.tar.gz"

    version('0.110', sha256='366117cb2966473f2559f2f4575ff6ae69e84c69a0f30a0773e1b51a457ef5c3')

    depends_on('perl-sub-install', type=('build', 'run'))
