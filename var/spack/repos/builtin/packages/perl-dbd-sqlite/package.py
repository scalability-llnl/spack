# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDbdSqlite(PerlPackage):
    """DBD::SQLite - Self-contained RDBMS in a DBI Driver"""

    homepage = "https://metacpan.org/pod/DBD::SQLite"
    url = "https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/DBD-SQLite-1.58.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.74", sha256="8994997d84b9feb4547795f78746c661fb72e3cb6a25dbdd789b731f5688a4dd")
    version("1.72", sha256="5ca41e61eb52b52bd862a3088b912a75fe70910ac789b9a9983e0a449e94f551")
    version("1.59_01", sha256="b6f331e4054688572c2010e72c355f7ba3f30d86051e50d9925d34d9df1001e2")
    version("1.58", sha256="7120dd99d0338dea2802fda8bfe3fbf10077d5af559f6c67ae35e9270d1a1d3b")
    version("1.57_01", sha256="fa7fb111fa8bfc257c3208f8980ac802a9cac4531ab98afc1988b88929672184")
    version("1.56", sha256="c5f831a67a94f9bb2fb3c44051f309fc7994b2725d1896c018ad5d4cd865e991")

    depends_on("c", type="build")  # generated

    depends_on("perl-dbi", type=("build", "run"))
