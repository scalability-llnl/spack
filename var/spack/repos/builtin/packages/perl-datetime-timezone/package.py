# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDatetimeTimezone(PerlPackage):
    """DateTime::TimeZone - Time zone object base class and factory"""

    homepage = "https://metacpan.org/pod/DateTime::TimeZone"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/DateTime-TimeZone-2.60.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.60", sha256="f0460d379323905b579bed44e141237a337dc25dd26b6ab0c60ac2b80629323d")

    depends_on("perl@5.8.4:", type=("build", "link", "run", "test"))
    depends_on("perl-class-singleton@1.03:", type=("build", "run", "test"))
    depends_on("perl-module-runtime", type=("build", "run", "test"))
    depends_on("perl-namespace-autoclean", type=("build", "run", "test"))
    depends_on("perl-params-validationcompiler@0.13:", type=("build", "run", "test"))
    depends_on("perl-specio", type=("build", "run", "test"))
    depends_on("perl-test-fatal", type=("build", "test"))
    depends_on("perl-test-requires", type=("build", "test"))
    depends_on("perl-try-tiny", type=("build", "run", "test"))
