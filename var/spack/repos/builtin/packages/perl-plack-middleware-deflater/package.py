# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPlackMiddlewareDeflater(PerlPackage):
    """Compress response body with Gzip or Deflate"""

    homepage = "https://metacpan.org/pod/Plack::Middleware::Deflater"
    url = (
        "https://cpan.metacpan.org/authors/id/K/KA/KAZEBURO/Plack-Middleware-Deflater-0.12.tar.gz"
    )

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.12", sha256="28da95e7da4c8b5591ac454509c92176cd0842960ce074fde30f9a1075dcc275")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-plack", type=("build", "run", "test"))
    depends_on("perl-test-requires", type=("build", "link"))
