# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPodCoverage(PerlPackage):
    """Checks if the documentation of a module is comprehensive"""

    homepage = "https://metacpan.org/pod/Pod::Coverage"
    url = "https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/Pod-Coverage-0.23.tar.gz"

    maintainers("EbiArnie")

    version("0.23", sha256="30b7a0b0c942f44a7552c0d34e9b1f2e0ba0b67955c61e3b1589ec369074b107")

    depends_on("perl-devel-symdump@2.01:", type=("build", "run", "test"))
    depends_on("perl-pod-parser@1.13:", type=("build", "run", "test"))
