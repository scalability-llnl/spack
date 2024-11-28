# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCriticMoose(PerlPackage):
    """Policies for Perl::Critic concerned with using Moose"""

    homepage = "https://metacpan.org/pod/Perl::Critic::Moose"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Perl-Critic-Moose-1.05.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.05", sha256="52eb8e22c42643f17fe297a21714017efdb9e2986c24e3337e030f3650f92201")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
    depends_on("perl-namespace-autoclean", type=("build", "run", "test"))
    depends_on("perl-perl-critic", type=("build", "run", "test"))
    depends_on("perl-readonly", type=("build", "run", "test"))
