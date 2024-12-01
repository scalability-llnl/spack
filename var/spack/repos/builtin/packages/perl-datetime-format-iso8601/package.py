# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDatetimeFormatIso8601(PerlPackage):
    """Parses ISO8601 formats"""

    homepage = "https://metacpan.org/pod/DateTime::Format::ISO8601"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/DateTime-Format-ISO8601-0.16.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.16", sha256="582847f6e029065334a00564f20cd7c28f4e5cd4ec21513d0f692531ed3b56e1")

    depends_on("perl-datetime@1.45:", type=("build", "run", "test"))
    depends_on("perl-datetime-format-builder@0.77:", type=("build", "run", "test"))
    depends_on("perl-namespace-autoclean", type=("build", "run", "test"))
    depends_on("perl-params-validationcompiler@0.26:", type=("build", "run", "test"))
    depends_on("perl-specio@0.18:", type=("build", "run", "test"))
    depends_on("perl-test2-suite", type=("build", "test"))
