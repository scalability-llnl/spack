# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestSubcalls(PerlPackage):
    """Track the number of times subs are called"""

    homepage = "https://metacpan.org/pod/Test::SubCalls"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Test-SubCalls-1.10.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.10", sha256="cbc1e9b35a05e71febc13e5ef547a31c8249899bb6011dbdc9d9ff366ddab6c2")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-hook-lexwrap@0.20:", type=("build", "run", "test"))
