# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlRoseDbObject(PerlPackage):
    """Extensible, high performance object-relational mapper (ORM)."""

    homepage = "https://metacpan.org/pod/Rose::DB::Object"
    url = "https://cpan.metacpan.org/authors/id/J/JS/JSIRACUSA/Rose-DB-Object-0.820.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.820", sha256="a0077609250966636f1411bcce2493cf1e1166ba935071738eb4b713104da83b")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-bit-vector", type=("build", "run", "test"))
    depends_on("perl-clone@0.29:", type=("build", "run", "test"))
    depends_on("perl-datetime", type=("build", "run", "test"))
    depends_on("perl-dbi@1.40:", type=("build", "run", "test"))
    depends_on("perl-list-moreutils", type=("build", "run", "test"))
    depends_on("perl-rose-datetime", type=("build", "run", "test"))
    depends_on("perl-rose-db@0.782:", type=("build", "run", "test"))
    depends_on("perl-rose-object@0.854:", type=("build", "run", "test"))
    depends_on("perl-time-clock@1.00:", type=("build", "run", "test"))
