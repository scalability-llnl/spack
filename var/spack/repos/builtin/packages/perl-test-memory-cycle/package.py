# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestMemoryCycle(PerlPackage):
    """Check for memory leaks and circular memory references"""

    homepage = "https://metacpan.org/pod/Test::Memory::Cycle"
    url = "http://search.cpan.org/CPAN/authors/id/P/PE/PETDANCE/Test-Memory-Cycle-1.06.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.06", sha256="9d53ddfdc964cd8454cb0da4c695b6a3ae47b45839291c34cb9d8d1cfaab3202")

    depends_on("perl-padwalker", type=("build", "run"))
    depends_on("perl-devel-cycle", type=("build", "run"))
