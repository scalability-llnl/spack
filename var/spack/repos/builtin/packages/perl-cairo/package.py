# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCairo(PerlPackage):
    """Perl interface to the cairo 2d vector graphics library"""

    homepage = "http://search.cpan.org/~xaoc/Cairo/lib/Cairo.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/X/XA/XAOC/Cairo-1.106.tar.gz"

    version('1.106', sha256='e64803018bc7cba49e73e258547f5378cc4249797beafec524852140f49c45c4')

    depends_on('cairo')
    depends_on('perl-extutils-depends')
    depends_on('perl-extutils-pkgconfig')
