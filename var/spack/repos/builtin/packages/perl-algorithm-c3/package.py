# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlAlgorithmC3(PerlPackage):
    """A module for merging hierarchies using the C3 algorithm"""

    homepage = "https://metacpan.org/pod/Algorithm::C3"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Algorithm-C3-0.11.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.11", sha256="aaf48467765deea6e48054bc7d43e46e4d40cbcda16552c629d37be098289309")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
