# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestPerlCritic(PerlPackage):
    """Use Perl::Critic in test programs."""

    homepage = "https://metacpan.org/pod/Test::Perl::Critic"
    url = "https://cpan.metacpan.org/authors/id/P/PE/PETDANCE/Test-Perl-Critic-1.04.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.04", sha256="28f806b5412c7908b56cf1673084b8b44ce1cb54c9417d784d91428e1a04096e")

    depends_on("perl-mce@1.827:", type=("build", "run", "test"))
    depends_on("perl-perl-critic@1.105:", type=("build", "run", "test"))
