# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFontTtf(PerlPackage):
    """Perl module for TrueType Font hacking"""

    homepage = "https://metacpan.org/pod/Font::TTF"
    url = "http://search.cpan.org/CPAN/authors/id/B/BH/BHALLISSY/Font-TTF-1.06.tar.gz"

    version("1.06", sha256="4b697d444259759ea02d2c442c9bffe5ffe14c9214084a01f743693a944cc293")
