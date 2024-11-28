# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSearchElasticsearch(PerlPackage):
    """The official client for Elasticsearch"""

    homepage = "https://metacpan.org/pod/Search::Elasticsearch"
    url = "https://cpan.metacpan.org/authors/id/E/EZ/EZIMUEL/Search-Elasticsearch-8.00.tar.gz"

    maintainers("EbiArnie")

    license("Apache-2.0")

    version("8.00", sha256="4b95357072b7432e02cc9ef897881976650e03030c15ec752789299284ce30ab")

    depends_on("perl-any-uri-escape", type=("build", "run", "test"))
    depends_on("perl-devel-globaldestruction", type=("build", "run", "test"))
    depends_on("perl-http-message", type=("build", "run", "test"))
    depends_on("perl-io-socket-ssl", type=("build", "test"))
    depends_on("perl-json-maybexs@1.002002:", type=("build", "run", "test"))
    depends_on("perl-libwww-perl", type=("build", "run", "test"))
    depends_on("perl-log-any@1.02:", type=("build", "run", "test"))
    depends_on("perl-log-any-adapter-callback@0.09:", type=("build", "test"))
    depends_on("perl-module-runtime", type=("build", "run", "test"))
    depends_on("perl-moo@2.001000:", type=("build", "run", "test"))
    depends_on("perl-namespace-clean", type=("build", "run", "test"))
    depends_on("perl-net-ip", type=("build", "run", "test"))
    depends_on("perl-package-stash@0.34:", type=("build", "run", "test"))
    depends_on("perl-sub-exporter", type=("build", "run", "test"))
    depends_on("perl-test-deep", type=("build", "test"))
    depends_on("perl-test-exception", type=("build", "test"))
    depends_on("perl-test-pod", type=("build", "test"))
    depends_on("perl-test-sharedfork", type=("build", "test"))
    depends_on("perl-try-tiny", type=("build", "run", "test"))
    depends_on("perl-uri", type=("build", "run", "test"))
