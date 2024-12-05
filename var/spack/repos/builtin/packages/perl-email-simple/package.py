# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlEmailSimple(PerlPackage):
    """Simple parsing of RFC2822 message format and headers"""

    homepage = "https://metacpan.org/pod/Email::Simple"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Email-Simple-2.218.tar.gz"

    maintainers("EbiArnie")

    version("2.218", sha256="2dce1d68fde99d53db9ca43e211b69b169ba2efaecf87a55cb33a9336047c96d")

    depends_on("perl@5.12.0:", type=("build", "link", "run", "test"))
    depends_on("perl-email-date-format", type=("build", "run", "test"))
