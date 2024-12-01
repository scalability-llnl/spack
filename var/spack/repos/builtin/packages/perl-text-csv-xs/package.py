# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTextCsvXs(PerlPackage):
    """Comma-Separated Values manipulation routines"""

    homepage = "https://metacpan.org/pod/Text::CSV_XS"
    url = "https://cpan.metacpan.org/authors/id/H/HM/HMBRAND/Text-CSV_XS-1.53.tgz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.53", sha256="ba3231610fc755a69e14eb4a3c6d8cce46cc4fd32853777a6c9ce485a8878b42")

    depends_on("perl@5.6.1:", type=("build", "link", "run", "test"))
