# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPlackMiddlewareFixmissingbodyinredirect(PerlPackage):
    """Plack::Middleware which sets body for redirect response, if it's not already set"""

    homepage = "https://metacpan.org/pod/Plack::Middleware::FixMissingBodyInRedirect"
    url = "https://cpan.metacpan.org/authors/id/S/SW/SWEETKID/Plack-Middleware-FixMissingBodyInRedirect-0.12.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.12", sha256="6c22d069f5a57ac206d4659b28b8869bb9270640bb955efddd451dcc58cdb391")

    depends_on("perl-html-parser", type=("build", "run", "test"))
    depends_on("perl-http-message", type=("build", "test"))
    depends_on("perl-plack", type=("build", "run", "test"))
