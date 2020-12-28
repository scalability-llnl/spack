# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlParserLite(PerlPackage):
    """Lightweight pure-perl XML Parser (based on regexps)"""

    homepage = "http://search.cpan.org/~phred/XML-Parser-Lite-0.721/lib/XML/Parser/Lite.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PH/PHRED/XML-Parser-Lite-0.721.tar.gz"

    version('0.721', sha256='5862a36ecab9db9aad021839c847e8d2f4ab5a7796c61d0fb069bb69cf7908ba')

    depends_on('perl-test-requires', type=('build', 'run'))
