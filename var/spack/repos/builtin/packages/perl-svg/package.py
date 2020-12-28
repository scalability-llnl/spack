# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSvg(PerlPackage):
    """Perl extension for generating Scalable Vector Graphics (SVG) documents.
    """

    homepage = "http://search.cpan.org/~manwar/SVG-2.78/lib/SVG.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MA/MANWAR/SVG-2.78.tar.gz"

    version('2.78', sha256='a665c1f18c0529f3da0f4b631976eb47e0f71f6d6784ef3f44d32fd76643d6bb')
