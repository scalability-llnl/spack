# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSpecio(PerlPackage):
    """Type constraints and coercions for Perl ."""

    homepage = "https://metacpan.org/dist/Specio"
    url = "http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Specio-0.48.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-2.0")

    version("0.48", sha256="0c85793580f1274ef08173079131d101f77b22accea7afa8255202f0811682b2")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
    depends_on("perl-devel-stacktrace", type=("build", "run", "test"))
    depends_on("perl-eval-closure", type=("build", "run", "test"))
    depends_on("perl-module-runtime", type=("build", "run", "test"))
    depends_on("perl-mro-compat", type=("build", "run", "test"))
    depends_on("perl-role-tiny@1.003003:", type=("build", "run", "test"))
    depends_on("perl-sub-quote", type=("build", "run", "test"))
    depends_on("perl-test-fatal", type=("build", "run", "test"))
    depends_on("perl-test-needs", type=("build", "test"))
    depends_on("perl-try-tiny", type=("build", "run", "test"))
