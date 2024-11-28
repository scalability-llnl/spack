# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlWwwFormUrlencoded(PerlPackage):
    """Parser and builder for application/x-www-form-urlencoded"""

    homepage = "https://metacpan.org/pod/WWW::Form::UrlEncoded"
    url = "https://cpan.metacpan.org/authors/id/K/KA/KAZEBURO/WWW-Form-UrlEncoded-0.26.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.26", sha256="c0480b5f1f15b71163ec327b8e7842298f0cb3ace97e63d7034af1e94a2d90f4")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
