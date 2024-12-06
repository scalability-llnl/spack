# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlTidy(PerlPackage):
    """Indent and reformat perl scripts"""

    homepage = "https://metacpan.org/pod/Perl::Tidy"
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHANCOCK/Perl-Tidy-20240202.tar.gz"

    maintainers("EbiArnie")

    license("GPL-2.0-only")

    version("20240202", sha256="9451adde47c2713652d39b150fb3eeb3ccc702add46913e989125184cd7ec57d")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
