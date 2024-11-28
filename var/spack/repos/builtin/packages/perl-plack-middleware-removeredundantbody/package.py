# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPlackMiddlewareRemoveredundantbody(PerlPackage):
    """Plack::Middleware which removes body for HTTP response if it's not required"""

    homepage = "https://metacpan.org/pod/Plack::Middleware::RemoveRedundantBody"
    url = "https://cpan.metacpan.org/authors/id/S/SW/SWEETKID/Plack-Middleware-RemoveRedundantBody-0.09.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.09", sha256="80d45f93d6b7290b0bd8b3cedd84a37fc501456cc3dec02ec7aad81c0018087e")

    depends_on("perl-http-message", type=("build", "test"))
    depends_on("perl-plack", type=("build", "run", "test"))
