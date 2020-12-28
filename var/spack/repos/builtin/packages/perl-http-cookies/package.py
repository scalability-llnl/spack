# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpCookies(PerlPackage):
    """HTTP cookie jars"""

    homepage = "http://search.cpan.org/~oalders/HTTP-Cookies-6.04/lib/HTTP/Cookies.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/HTTP-Cookies-6.04.tar.gz"

    version('6.04', sha256='0cc7f079079dcad8293fea36875ef58dd1bfd75ce1a6c244cd73ed9523eb13d4')

    depends_on('perl-uri', type=('build', 'run'))
    depends_on('perl-http-message', type=('build', 'run'))
