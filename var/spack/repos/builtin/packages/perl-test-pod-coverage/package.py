# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestPodCoverage(PerlPackage):
    """Check for pod coverage in your distribution"""

    homepage = "https://metacpan.org/pod/Test::Pod::Coverage"
    url = "https://cpan.metacpan.org/authors/id/N/NE/NEILB/Test-Pod-Coverage-1.10.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-2.0")

    version("1.10", sha256="48c9cca9f7d99eee741176445b431adf09c029e1aa57c4703c9f46f7601d40d4")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-pod-coverage", type=("build", "run", "test"))
