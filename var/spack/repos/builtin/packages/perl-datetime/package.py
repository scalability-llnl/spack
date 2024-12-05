# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDatetime(PerlPackage):
    """DateTime - A date and time object for Perl"""

    homepage = "https://metacpan.org/pod/DateTime"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/DateTime-1.65.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-2.0")

    version("1.65", sha256="0bfda7ff0253fb3d88cf4bdb5a14afb8cea24d147975d5bdf3c88b40e7ab140e")
    version(
        "1.63",
        sha256="1b11e49ec6e184ae2a10eccd05eda9534f32458fc644c12ab710c29a3a816f6f",
        deprecated=True,
    )

    depends_on("perl@5.8.4:", type=("build", "link", "run", "test"))
    depends_on("perl-cpan-meta-check@0.011:", type=("build", "test"))
    depends_on("perl-datetime-locale@1.06:", type=("build", "run", "test"))
    depends_on("perl-datetime-timezone@2.44:", type=("build", "run", "test"))
    depends_on("perl-dist-checkconflicts@0.02:", type=("build", "run", "test"))
    depends_on("perl-namespace-autoclean@0.19:", type=("build", "run", "test"))
    depends_on("perl-params-validationcompiler@0.26:", type=("build", "run", "test"))
    depends_on("perl-specio@0.18:", type=("build", "run", "test"))
    depends_on("perl-test-fatal", type=("build", "test"))
    depends_on("perl-test-warnings@0.005:", type=("build", "test"))
    depends_on("perl-test-without-module", type=("build", "test"))
    depends_on("perl-try-tiny", type=("build", "run", "test"))
