# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDbFile(PerlPackage):
    """DB_File is a module which allows Perl programs to make use of the
    facilities provided by Berkeley DB version 1.x (if you have a newer version
    of DB, see "Using DB_File with Berkeley DB version 2 or greater").
    It is assumed that you have a copy of the Berkeley DB manual pages at hand
    when reading this documentation. The interface defined here mirrors the
    Berkeley DB interface closely."""

    homepage = "https://metacpan.org/pod/DB_File"
    url = "https://cpan.metacpan.org/authors/id/P/PM/PMQS/DB_File-1.840.tar.gz"

    version("1.859", sha256="5674e0d2cd0b060c4d1253670ea022c64d842a55257f9eb8edb19c0f53e2565c")
    version("1.858", sha256="ceb7a2868bd71f87b31e8b7c38d6f8cc0a31fb0322a377ee448994f094d0a7f6")
    version("1.840", sha256="b7864707fad0f2d1488c748c4fa08f1fb8bcfd3da247c36909fd42f20bfab2c4")

    depends_on("c", type="build")  # generated

    depends_on("perl-extutils-makemaker", type="build")
    depends_on("berkeley-db", type="build")

    def patch(self):
        filter_file("/usr/local/BerkeleyDB", self.spec["berkeley-db"].prefix, "config.in")
