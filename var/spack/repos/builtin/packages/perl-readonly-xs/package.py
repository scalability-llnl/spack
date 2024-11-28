# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlReadonlyXs(PerlPackage):
    """Companion module for Readonly.pm, to speed up read-only scalar variables."""

    homepage = "https://metacpan.org/pod/Readonly::XS"
    url = "https://cpan.metacpan.org/authors/id/R/RO/ROODE/Readonly-XS-1.05.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.05", sha256="8ae5c4e85299e5c8bddd1b196f2eea38f00709e0dc0cb60454dc9114ae3fff0d")

    depends_on("perl-readonly@1.02:", type=("build", "run", "test"))
