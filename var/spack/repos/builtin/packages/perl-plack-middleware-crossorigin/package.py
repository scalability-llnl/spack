# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPlackMiddlewareCrossorigin(PerlPackage):
    """Adds headers to allow Cross-Origin Resource Sharing"""

    homepage = "https://metacpan.org/pod/Plack::Middleware::CrossOrigin"
    url = (
        "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Plack-Middleware-CrossOrigin-0.014.tar.gz"
    )

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.014", sha256="35e80fabcc8455a6bc1aee0820fde9c4ae94baab7a795ce79932abc93004f3b7")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
    depends_on("perl-plack", type=("build", "run", "test"))
