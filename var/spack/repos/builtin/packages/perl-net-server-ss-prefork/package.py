# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNetServerSsPrefork(PerlPackage):
    """A hot-deployable variant of Net::Server::PreFork"""

    homepage = "https://metacpan.org/pod/Net::Server::SS::PreFork"
    url = "https://cpan.metacpan.org/authors/id/K/KA/KAZUHO/Net-Server-SS-PreFork-0.05.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.05", sha256="6d22b3a84eb3e01fb238f566bdb3014847d30e0d51ec1e86a0b6e043e367968b")

    depends_on("perl-http-server-simple", type=("build", "link"))
    depends_on("perl-libwww-perl", type=("build", "link"))
    depends_on("perl-net-server", type=("build", "run", "test"))
    depends_on("perl-server-starter@0.02:", type=("build", "run", "test"))
    depends_on("perl-test-tcp@0.06:", type=("build", "link"))
