# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPdfApi2(PerlPackage):
    """Facilitates the creation and modification of PDF files"""

    homepage = "https://metacpan.org/pod/PDF::API2"
    url = "http://search.cpan.org/CPAN/authors/id/S/SS/SSIMMS/PDF-API2-2.033.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.044", sha256="b2d15579e42723d8d7f9b72de86d0d35cde34f1eb7713456ba2ad35fb3cbea7e")
    version("2.033", sha256="9c0866ec1a3053f73afaca5f5cdbe6925903b4ce606f4bf4ac317731a69d27a0")

    depends_on("perl-test-exception", type=("build", "run"))
    depends_on("perl-test-memory-cycle", type=("build", "run"))
    depends_on("perl-font-ttf", type=("build", "run"))
