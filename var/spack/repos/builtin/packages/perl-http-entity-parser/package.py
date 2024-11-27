# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpEntityParser(PerlPackage):
    """PSGI compliant HTTP Entity Parser"""

    homepage = "https://metacpan.org/pod/HTTP::Entity::Parser"
    url = "https://cpan.metacpan.org/authors/id/K/KA/KAZEBURO/HTTP-Entity-Parser-0.25.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.25", sha256="3a8cd0d8cba3d17cd8c04ee82d7341dfaa247dbdd94a49eb94b53f69e483ec3a")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-hash-multivalue", type=("build", "run", "test"))
    depends_on("perl-http-message@6:", type=("build", "test"))
    depends_on("perl-http-multipartparser", type=("build", "run", "test"))
    depends_on("perl-json-maybexs@1.003007:", type=("build", "run", "test"))
    depends_on("perl-module-build-tiny@0.035:", type=("build"))
    depends_on("perl-stream-buffered", type=("build", "run", "test"))
    depends_on("perl-www-form-urlencoded@0.23:", type=("build", "run", "test"))
