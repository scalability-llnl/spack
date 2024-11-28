# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlUriWs(PerlPackage):
    """WebSocket support for URI package"""

    homepage = "https://metacpan.org/pod/URI::ws"
    url = "https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/URI-ws-0.03.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.03", sha256="6e6b0e4172acb6a53c222639c000608c2dd61d50848647482ac8600d50e541ef")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-uri", type=("build", "run", "test"))
