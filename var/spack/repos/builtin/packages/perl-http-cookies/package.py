# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpCookies(PerlPackage):
    """HTTP cookie jars"""

    homepage = "https://metacpan.org/pod/HTTP::Cookies"
    url = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/HTTP-Cookies-6.04.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("6.11", sha256="8c9a541a4a39f6c0c7e3d0b700b05dfdb830bd490a1b1942a7dedd1b50d9a8c8")
    version("6.10", sha256="e36f36633c5ce6b5e4b876ffcf74787cc5efe0736dd7f487bdd73c14f0bd7007")
    version("6.04", sha256="0cc7f079079dcad8293fea36875ef58dd1bfd75ce1a6c244cd73ed9523eb13d4")

    depends_on("perl-uri", type=("build", "run"))
    depends_on("perl-http-message", type=("build", "run"))
