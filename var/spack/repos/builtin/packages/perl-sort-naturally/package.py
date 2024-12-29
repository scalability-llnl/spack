# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSortNaturally(PerlPackage):
    """Sort lexically, but sort numeral parts numerically"""

    homepage = "https://metacpan.org/pod/Sort::Naturally"
    url = "https://cpan.metacpan.org/authors/id/B/BI/BINGOS/Sort-Naturally-1.03.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.03", sha256="eaab1c5c87575a7826089304ab1f8ffa7f18e6cd8b3937623e998e865ec1e746")

    depends_on("perl@5.0.0:", type=("build", "link", "run", "test"))

    use_modules = ["Sort::Naturally"]
