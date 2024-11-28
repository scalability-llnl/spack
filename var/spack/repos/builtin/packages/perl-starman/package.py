# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStarman(PerlPackage):
    """High-performance preforking PSGI/Plack web server"""

    homepage = "https://metacpan.org/pod/Starman"
    url = "https://cpan.metacpan.org/authors/id/M/MI/MIYAGAWA/Starman-0.4017.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.4017", sha256="6ffab915f323f60089e3ebf852b9b9707d6917266df8afd7370fac04bfdfee4e")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-data-dump", type=("build", "run", "test"))
    depends_on("perl-http-date", type=("build", "run", "test"))
    depends_on("perl-http-message", type=("build", "run", "test"))
    depends_on("perl-http-parser-xs", type=("build", "run", "test"))
    depends_on("perl-libwww-perl", type=("build", "test"))
    depends_on("perl-module-build-tiny@0.034:", type=("build"))
    depends_on("perl-net-server@2.007:", type=("build", "run", "test"))
    depends_on("perl-plack@0.9971:", type=("build", "run", "test"))
    depends_on("perl-test-requires", type=("build", "test"))
    depends_on("perl-test-tcp@2.00:", type=("build", "run", "test"))
