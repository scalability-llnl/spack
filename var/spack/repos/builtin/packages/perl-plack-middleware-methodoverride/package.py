# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPlackMiddlewareMethodoverride(PerlPackage):
    """Override REST methods to Plack apps via POST"""

    homepage = "https://metacpan.org/pod/Plack::Middleware::MethodOverride"
    url = "https://cpan.metacpan.org/authors/id/M/MI/MIYAGAWA/Plack-Middleware-MethodOverride-0.20.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.20", sha256="dbfb5a2efb48bfeb01cb3ae1e1c677e155dc7bfe210c7e7f221bae3cb6aab5f1")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-plack", type=("build", "run", "test"))
    depends_on("perl-uri", type=("build", "test"))
