# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlRoseDb(PerlPackage):
    """A DBI wrapper and abstraction layer."""

    homepage = "https://metacpan.org/pod/Rose::DB"
    url = "https://cpan.metacpan.org/authors/id/J/JS/JSIRACUSA/Rose-DB-0.785.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.785", sha256="7849307d748d9672b42ef3cd78f83d44dec034cdc94f4d4251d2761e27c67a3c")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-bit-vector", type=("build", "run", "test"))
    depends_on("perl-clone-pp", type=("build", "run", "test"))
    depends_on("perl-datetime", type=("build", "run", "test"))
    depends_on("perl-datetime-format-mysql", type=("build", "run", "test"))
    depends_on("perl-datetime-format-oracle", type=("build", "run", "test"))
    depends_on("perl-datetime-format-pg@0.11:", type=("build", "run", "test"))
    depends_on("perl-dbi", type=("build", "run", "test"))
    depends_on("perl-rose-datetime", type=("build", "run", "test"))
    depends_on("perl-rose-object@0.854:", type=("build", "run", "test"))
    depends_on("perl-sql-reservedwords", type=("build", "run", "test"))
    depends_on("perl-time-clock", type=("build", "run", "test"))
