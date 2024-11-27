# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMooxTypesMooselikeNumeric(PerlPackage):
    """Moo types for numbers"""

    homepage = "https://metacpan.org/pod/MooX::Types::MooseLike::Numeric"
    url = (
        "https://cpan.metacpan.org/authors/id/M/MA/MATEU/MooX-Types-MooseLike-Numeric-1.03.tar.gz"
    )

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.03", sha256="16adeb617b963d010179922c2e4e8762df77c75232e17320b459868c4970c44b")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-moo@1.004002:", type=("build", "link"))
    depends_on("perl-moox-types-mooselike@0.23:", type=("build", "run", "test"))
    depends_on("perl-test-fatal@0.003:", type=("build", "link"))
