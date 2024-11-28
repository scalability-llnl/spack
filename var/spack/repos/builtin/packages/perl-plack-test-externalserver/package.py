# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPlackTestExternalserver(PerlPackage):
    """Run HTTP tests on external live servers"""

    homepage = "https://metacpan.org/pod/Plack::Test::ExternalServer"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Plack-Test-ExternalServer-0.02.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.02", sha256="5baf5c57fe0c06412deec9c5abe7952ab8a04f8c47b4bbd8e9e9982268903ed0")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-http-message", type=("build", "test"))
    depends_on("perl-libwww-perl", type=("build", "run", "test"))
    depends_on("perl-plack", type=("build", "test"))
    depends_on("perl-test-tcp", type=("build", "test"))
    depends_on("perl-uri", type=("build", "run", "test"))
