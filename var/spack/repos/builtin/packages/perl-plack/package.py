# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPlack(PerlPackage):
    """Perl Superglue for Web frameworks and Web Servers (PSGI toolkit)"""

    homepage = "https://metacpan.org/pod/Plack"
    url = "https://cpan.metacpan.org/authors/id/M/MI/MIYAGAWA/Plack-1.0051.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.0051", sha256="bebde91c42298ed6ec8e6c82b21433a1b49aa39412c247f3905b80f955acf77b")

    depends_on("perl@5.12.0:", type=("build", "link", "run", "test"))
    depends_on("perl-apache-logformat-compiler@0.33:", type=("build", "run", "test"))
    depends_on("perl-cookie-baker@0.07:", type=("build", "run", "test"))
    depends_on("perl-devel-stacktrace@1.23:", type=("build", "run", "test"))
    depends_on("perl-devel-stacktrace-ashtml@0.11:", type=("build", "run", "test"))
    depends_on("perl-file-sharedir@1.00:", type=("build", "run", "test"))
    depends_on("perl-file-sharedir-install@0.06:", type=("build"))
    depends_on("perl-filesys-notify-simple", type=("build", "run", "test"))
    depends_on("perl-hash-multivalue@0.05:", type=("build", "run", "test"))
    depends_on("perl-http-entity-parser@0.25:", type=("build", "run", "test"))
    depends_on("perl-http-headers-fast@0.18:", type=("build", "run", "test"))
    depends_on("perl-http-message@5.814:", type=("build", "run", "test"))
    depends_on("perl-stream-buffered@0.02:", type=("build", "run", "test"))
    depends_on("perl-test-requires", type=("build", "test"))
    depends_on("perl-test-tcp@2.15:", type=("build", "run", "test"))
    depends_on("perl-try-tiny", type=("build", "run", "test"))
    depends_on("perl-uri@1.59:", type=("build", "run", "test"))
    depends_on("perl-www-form-urlencoded@0.23:", type=("build", "run", "test"))
