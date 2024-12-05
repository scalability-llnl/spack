# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerl6Slurp(PerlPackage):
    """Perl6::Slurp - Implements the Perl 6 'slurp' built-in"""

    homepage = "https://metacpan.org/pod/Perl6::Slurp"
    url = "http://search.cpan.org/CPAN/authors/id/D/DC/DCONWAY/Perl6-Slurp-0.051005.tar.gz"

    version("0.051005", sha256="0e0ceb30495ecf64dc6cacd12113d604871104c0cfe153487b8d68bc9393d78f")

    depends_on("perl@5.8:5", type=("build", "run"))
