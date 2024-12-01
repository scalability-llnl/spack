# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCgi(PerlPackage):
    """CGI - Handle Common Gateway Interface requests and responses

    CGI was included in the Perl distribution from 5.4 to 5.20 but
    has since been removed."""

    homepage = "https://metacpan.org/pod/CGI"
    url = "https://cpan.metacpan.org/authors/id/L/LE/LEEJO/CGI-4.40.tar.gz"

    maintainers("cessenat")

    license("Artistic-2.0")

    version("4.56", sha256="2d36d930b89ecdfbcc7d6d4740821bd466a0218abf1bd413568640b2f43799b7")
    version("4.54", sha256="9608a044ae2e87cefae8e69b113e3828552ddaba0d596a02f9954c6ac17fa294")
    version("4.53", sha256="c67e732f3c96bcb505405fd944f131fe5c57b46e5d02885c00714c452bf14e60")
    version("4.40", sha256="10efff3061b3c31a33b3cc59f955aef9c88d57d12dbac46389758cef92f24f56")
    version("4.39", sha256="7e73417072445f24e03d63802ed3a9e368c9b103ddc96e2a9bcb6a251215fb76")
    version("4.38", sha256="8c58f4a529bb92a914b22b7e64c5e31185c9854a4070a6dfad44fe5cc248e7d4")
    version("4.37", sha256="7a14eee5df640f7141848f653cf48d99bfc9b5c68e18167338ee01b91cdfb883")

    depends_on("perl-html-parser", type=("build", "run"))
