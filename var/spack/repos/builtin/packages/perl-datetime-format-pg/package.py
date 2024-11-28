# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDatetimeFormatPg(PerlPackage):
    """Parse and format PostgreSQL dates and times"""

    homepage = "https://metacpan.org/pod/DateTime::Format::Pg"
    url = "https://cpan.metacpan.org/authors/id/D/DM/DMAKI/DateTime-Format-Pg-0.16014.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.16014", sha256="38bb9666524dc384c3366f6342cb9656c50bac0f9716a3d44f1cf552ccbe0eb9")

    depends_on("perl-datetime@0.10:", type=("build", "run", "test"))
    depends_on("perl-datetime-format-builder@0.72:", type=("build", "run", "test"))
    depends_on("perl-datetime-timezone@0.05:", type=("build", "run", "test"))
    depends_on("perl-module-build-tiny@0.035:", type=("build"))
