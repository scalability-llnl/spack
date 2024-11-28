# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTermTable(PerlPackage):
    """Format a header and rows into a table"""

    homepage = "https://metacpan.org/pod/Term::Table"
    url = "https://cpan.metacpan.org/authors/id/E/EX/EXODIST/Term-Table-0.018.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.018", sha256="9159b9131ee6b3f3956b74f45422985553574babbfaeba60be5c17bc114ac011")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
