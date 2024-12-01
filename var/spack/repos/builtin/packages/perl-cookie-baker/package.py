# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCookieBaker(PerlPackage):
    """Cookie string generator / parser"""

    homepage = "https://metacpan.org/pod/Cookie::Baker"
    url = "https://cpan.metacpan.org/authors/id/K/KA/KAZEBURO/Cookie-Baker-0.12.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.12", sha256="9b04df5d47dcd45ac4299626a10ec990fb40c94ee5a6300c3a88bdfb3575ec29")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-module-build-tiny@0.035:", type=("build"))
    depends_on("perl-test-time", type=("build", "test"))
    depends_on("perl-uri", type=("build", "run", "test"))
