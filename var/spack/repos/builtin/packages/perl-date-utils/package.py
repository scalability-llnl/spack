# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDateUtils(PerlPackage):
    """Common date functions as Moo Role."""

    homepage = "https://metacpan.org/pod/Date::Utils"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MANWAR/Date-Utils-0.28.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-2.0")

    version("0.28", sha256="1ed50713512498e88a54bc7dcf70372763b63196ecf7d9a54668e535d22f03ad")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-date-exception@0.08:", type=("build", "run", "test"))
    depends_on("perl-moo", type=("build", "run", "test"))
    depends_on("perl-namespace-autoclean@0.28:", type=("build", "run", "test"))
    depends_on("perl-term-ansicolor-markup@0.06:", type=("build", "run", "test"))
