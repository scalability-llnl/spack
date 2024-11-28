# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSqlAbstractClassic(PerlPackage):
    """Generate SQL from Perl data structures"""

    homepage = "https://metacpan.org/pod/SQL::Abstract::Classic"
    url = "https://cpan.metacpan.org/authors/id/R/RI/RIBASUSHI/SQL-Abstract-Classic-1.91.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.91", sha256="4e3d1dfd095b2123268586bb06b86929ea571388d4e941acccbdcda1e108ef28")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-mro-compat@0.12:", type=("build", "run", "test"))
    depends_on("perl-sql-abstract@1.79:", type=("build", "run", "test"))
    depends_on("perl-test-deep@0.101:", type=("build", "link"))
    depends_on("perl-test-exception@0.31:", type=("build", "link"))
    depends_on("perl-test-warn", type=("build", "link"))
