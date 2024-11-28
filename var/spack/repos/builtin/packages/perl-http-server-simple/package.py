# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpServerSimple(PerlPackage):
    """Lightweight HTTP server"""

    homepage = "https://metacpan.org/pod/HTTP::Server::Simple"
    url = "https://cpan.metacpan.org/authors/id/B/BP/BPS/HTTP-Server-Simple-0.52.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.52", sha256="d8939fa4f12bd6b8c043537fd0bf96b055ac3686b9cdd9fa773dca6ae679cb4c")

    depends_on("perl-cgi", type=("build", "run", "test"))
