# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpRequestAscgi(PerlPackage):
    """Set up a CGI environment from an HTTP::Request"""

    homepage = "https://metacpan.org/pod/HTTP::Request::AsCGI"
    url = "https://cpan.metacpan.org/authors/id/F/FL/FLORA/HTTP-Request-AsCGI-1.2.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.2", sha256="945bfb07c6d1af52773fb7845ba62e3a74111b35cbd2d5e43ef8319e55acbcea")

    depends_on("perl-class-accessor", type=("build", "run", "test"))
    depends_on("perl-http-message", type=("build", "run", "test"))
    depends_on("perl-uri", type=("build", "run", "test"))
