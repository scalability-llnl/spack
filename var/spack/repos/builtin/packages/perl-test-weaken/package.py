# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestWeaken(PerlPackage):
    """Test that freed memory objects were, indeed, freed"""

    homepage = "https://metacpan.org/pod/Test::Weaken"
    url = "https://cpan.metacpan.org/authors/id/K/KR/KRYDE/Test-Weaken-3.022000.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("3.022000", sha256="2631a87121310262e0e96107a6fa0ed69487b7701520773bee5fa9accc295f5b")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
