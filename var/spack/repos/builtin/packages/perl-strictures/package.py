# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStrictures(PerlPackage):
    """Turn on strict and make most warnings fatal"""

    homepage = "https://metacpan.org/pod/strictures"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/strictures-2.000006.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("2.000006", sha256="09d57974a6d1b2380c802870fed471108f51170da81458e2751859f2714f8d57")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
