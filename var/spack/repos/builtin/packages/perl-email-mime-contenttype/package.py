# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlEmailMimeContenttype(PerlPackage):
    """Parse and build a MIME Content-Type or Content-Disposition Header"""

    homepage = "https://metacpan.org/pod/Email::MIME::ContentType"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Email-MIME-ContentType-1.028.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.028", sha256="e7950246433f7ed6c3e4fd4df2227e0f2341137c3cab1989018fc370f58145c4")

    depends_on("perl@5.12.0:", type=("build", "link", "run", "test"))
    depends_on("perl-text-unidecode", type=("build", "run", "test"))
