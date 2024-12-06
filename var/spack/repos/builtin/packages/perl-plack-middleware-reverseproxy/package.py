# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPlackMiddlewareReverseproxy(PerlPackage):
    """Supports app to run as a reverse proxy backend"""

    homepage = "https://metacpan.org/pod/Plack::Middleware::ReverseProxy"
    url = "https://cpan.metacpan.org/authors/id/M/MI/MIYAGAWA/Plack-Middleware-ReverseProxy-0.16.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.16", sha256="874931d37d07667ba0d0f37903b94511071f4191feb73fa45765da2b8c15a128")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-plack@0.9988:", type=("build", "run", "test"))
