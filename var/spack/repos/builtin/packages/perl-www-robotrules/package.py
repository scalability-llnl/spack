# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlWwwRobotrules(PerlPackage):
    """Database of robots.txt-derived permissions"""

    homepage = "http://deps.cpantesters.org/?module=WWW%3A%3ARobotRules;perl=latest"
    url = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/WWW-RobotRules-6.02.tar.gz"

    version("6.02", sha256="46b502e7a288d559429891eeb5d979461dd3ecc6a5c491ead85d165b6e03a51e")

    depends_on("perl-uri", type=("build", "run"))
