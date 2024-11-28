# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExporterAuto(PerlPackage):
    """Export all public functions from your package"""

    homepage = "https://metacpan.org/pod/Exporter::Auto"
    url = "https://cpan.metacpan.org/authors/id/N/NE/NEILB/Exporter-Auto-0.04.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.04", sha256="6009710ee628ca7d7c3bfa6721190ded4a7a5db2cdda789cd05731edc40edcd7")

    depends_on("perl@5.8.5:", type=("build", "link", "run", "test"))
    depends_on("perl-b-hooks-endofscope", type=("build", "run", "test"))
    depends_on("perl-sub-identify", type=("build", "run", "test"))
