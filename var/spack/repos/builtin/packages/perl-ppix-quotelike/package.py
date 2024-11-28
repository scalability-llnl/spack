# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPpixQuotelike(PerlPackage):
    """Parse Perl string literals and string-literal-like things."""

    homepage = "https://metacpan.org/pod/PPIx::QuoteLike"
    url = "https://cpan.metacpan.org/authors/id/W/WY/WYANT/PPIx-QuoteLike-0.023.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.023", sha256="3576a3149d2c53e07e9737b7892be5cfb84a499a6ef1df090b713b0544234d21")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-ppi", type=("build", "run", "test"))
    depends_on("perl-readonly", type=("build", "run", "test"))
