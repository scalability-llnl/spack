# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPdfApi2(PerlPackage):
    """Facilitates the creation and modification of PDF files"""

    homepage = "http://search.cpan.org/~ssimms/PDF-API2-2.033/lib/PDF/API2.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/S/SS/SSIMMS/PDF-API2-2.033.tar.gz"

    version('2.033', sha256='9c0866ec1a3053f73afaca5f5cdbe6925903b4ce606f4bf4ac317731a69d27a0')

    depends_on('perl-test-exception', type=('build', 'run'))
    depends_on('perl-test-memory-cycle', type=('build', 'run'))
    depends_on('perl-font-ttf', type=('build', 'run'))
