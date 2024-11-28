# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDbdPg(PerlPackage):
    """DBD::Pg is a Perl module that works with the DBI module to provide
    access to PostgreSQL databases."""

    homepage = "https://metacpan.org/pod/DBD::Pg"
    url = "https://cpan.metacpan.org/authors/id/T/TU/TURNSTEP/DBD-Pg-3.10.0.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("3.18.0", sha256="92bbe8a363040f8ce6a3f1963f128132e245861a9b4dc5a84178b42d625a7807")
    version("3.16.1", sha256="8e917a746dacb1edce5832d8911e5938cc4863aeac4a52820382e7d174e9c3b9")
    version("3.10.0", sha256="e103268a63e2828e3d43659bdba5f743446cbbe047a766f843112eedae105f80")

    depends_on("c", type="build")  # generated

    depends_on("postgresql")
    depends_on("perl-dbi", type=("build", "run"))
