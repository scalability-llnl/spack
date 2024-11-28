# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCatalystRuntime(PerlPackage):
    """The Catalyst Framework Runtime"""

    homepage = "https://metacpan.org/pod/Catalyst::Test"
    url = "https://cpan.metacpan.org/authors/id/J/JJ/JJNAPIORK/Catalyst-Runtime-5.90131.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("5.90131", sha256="9d641efacf0f9935e6ecb98f5a3b476c961b1f819bd2f8f23a647d1d867e1849")

    depends_on("perl@5.8.3:", type=("build", "link", "run", "test"))
    depends_on("perl-cgi-simple", type=("build", "run", "test"))
    depends_on("perl-cgi-struct", type=("build", "run", "test"))
    depends_on("perl-class-c3-adopt-next@0.07:", type=("build", "run", "test"))
    depends_on("perl-class-load@0.12:", type=("build", "run", "test"))
    depends_on("perl-data-dump", type=("build", "run", "test"))
    depends_on("perl-data-optlist", type=("build", "run", "test"))
    depends_on("perl-hash-multivalue", type=("build", "run", "test"))
    depends_on("perl-html-parser", type=("build", "run", "test"))
    depends_on("perl-http-body@1.22:", type=("build", "run", "test"))
    depends_on("perl-http-message", type=("build", "run", "test"))
    depends_on("perl-json-maybexs@1.000000:", type=("build", "run", "test"))
    depends_on("perl-libwww-perl@5.837:", type=("build", "run", "test"))
    depends_on("perl-module-pluggable@4.7:", type=("build", "run", "test"))
    depends_on("perl-moose@2.1400:", type=("build", "run", "test"))
    depends_on("perl-moosex-emulate-class-accessor-fast@0.00903:", type=("build", "run", "test"))
    depends_on("perl-moosex-getopt@0.48:", type=("build", "run", "test"))
    depends_on("perl-moosex-methodattributes", type=("build", "run", "test"))
    depends_on("perl-mro-compat", type=("build", "run", "test"))
    depends_on("perl-namespace-clean@0.23:", type=("build", "run", "test"))
    depends_on("perl-path-class@0.09:", type=("build", "run", "test"))
    depends_on("perl-perlio-utf8-strict", type=("build", "run", "test"))
    depends_on("perl-plack@0.9991:", type=("build", "run", "test"))
    depends_on(
        "perl-plack-middleware-fixmissingbodyinredirect@0.09:", type=("build", "run", "test")
    )
    depends_on("perl-plack-middleware-methodoverride@0.12:", type=("build", "run", "test"))
    depends_on("perl-plack-middleware-removeredundantbody@0.03:", type=("build", "run", "test"))
    depends_on("perl-plack-middleware-reverseproxy@0.04:", type=("build", "run", "test"))
    depends_on("perl-plack-test-externalserver", type=("build", "run", "test"))
    depends_on("perl-safe-isa", type=("build", "run", "test"))
    depends_on("perl-stream-buffered", type=("build", "run", "test"))
    depends_on("perl-string-rewriteprefix@0.004:", type=("build", "run", "test"))
    depends_on("perl-sub-exporter", type=("build", "run", "test"))
    depends_on("perl-task-weaken", type=("build", "run", "test"))
    depends_on("perl-test-fatal", type=("build", "test"))
    depends_on("perl-text-simpletable@0.03:", type=("build", "run", "test"))
    depends_on("perl-tree-simple@1.15:", type=("build", "run", "test"))
    depends_on("perl-tree-simple-visitorfactory", type=("build", "run", "test"))
    depends_on("perl-try-tiny@0.17:", type=("build", "run", "test"))
    depends_on("perl-uri@1.65:", type=("build", "run", "test"))
    depends_on("perl-uri-ws@0.03:", type=("build", "run", "test"))
