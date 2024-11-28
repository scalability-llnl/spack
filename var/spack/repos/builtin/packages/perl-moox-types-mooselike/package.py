# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMooxTypesMooselike(PerlPackage):
    """Some Moosish types and a type builder"""

    homepage = "https://metacpan.org/pod/MooX::Types::MooseLike"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MATEU/MooX-Types-MooseLike-0.29.tar.gz"

    maintainers("EbiArnie")

    version("0.29", sha256="1d3780aa9bea430afbe65aa8c76e718f1045ce788aadda4116f59d3b7a7ad2b4")

    depends_on("perl-module-runtime@0.014:", type=("build", "run", "test"))
    depends_on("perl-moo@1.004002:", type=("build", "test"))
    depends_on("perl-test-fatal@0.003:", type=("build", "test"))
