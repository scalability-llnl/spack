# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSqlAbstract(PerlPackage):
    """Generate SQL from Perl data structures"""

    homepage = "https://metacpan.org/pod/SQL::Abstract"
    url = "https://cpan.metacpan.org/authors/id/M/MS/MSTROUT/SQL-Abstract-2.000001.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("2.000001", sha256="35a642662c349420d44be6e0ef7d8765ea743eb12ad14399aa3a232bb94e6e9a")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-data-dumper-concise", type=("build", "test"))
    depends_on("perl-hash-merge@0.12:", type=("build", "run", "test"))
    depends_on("perl-moo@2.000001:", type=("build", "run", "test"))
    depends_on("perl-mro-compat@0.12:", type=("build", "run", "test"))
    depends_on("perl-sub-quote@2.000001:", type=("build", "run", "test"))
    depends_on("perl-test-deep@0.101:", type=("build", "run", "test"))
    depends_on("perl-test-exception@0.31:", type=("build", "test"))
    depends_on("perl-test-warn", type=("build", "test"))
