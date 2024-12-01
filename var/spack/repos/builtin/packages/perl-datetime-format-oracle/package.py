# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDatetimeFormatOracle(PerlPackage):
    """Parse and format Oracle dates and timestamps"""

    homepage = "https://metacpan.org/pod/DateTime::Format::Oracle"
    url = "https://cpan.metacpan.org/authors/id/K/KO/KOLIBRIE/DateTime-Format-Oracle-0.06.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.06", sha256="9f18d1eb3dff38e046ba063d6b54cc7d68464640ce69d7d1578a2ccd285ca8d4")

    depends_on("perl-convert-nls-date-format@0.03:", type=("build", "run", "test"))
    depends_on("perl-datetime", type=("build", "run", "test"))
    depends_on("perl-datetime-format-builder", type=("build", "run", "test"))
