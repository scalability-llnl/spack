# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestTcp(PerlPackage):
    """Testing TCP program"""

    homepage = "https://metacpan.org/pod/Test::TCP"
    url = "https://cpan.metacpan.org/authors/id/M/MI/MIYAGAWA/Test-TCP-2.22.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("2.22", sha256="3e53c3c06d6d0980a2bfeb915602b714e682ee211ae88c11748cf2cc714e7b57")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-test-sharedfork@0.29:", type=("build", "run", "test"))
