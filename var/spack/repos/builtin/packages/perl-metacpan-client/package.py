# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMetacpanClient(PerlPackage):
    """A comprehensive, DWIM-featured client to the MetaCPAN API"""

    homepage = "https://metacpan.org/pod/MetaCPAN::Client"
    url = "https://cpan.metacpan.org/authors/id/M/MI/MICKEY/MetaCPAN-Client-2.031000.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("2.031000", sha256="c6ceaf886a74120e2bffe2ec1f09d0fdc330acbfdb9ec876ef925ee687ec7cf5")

    depends_on("perl@5.10.0:", type=("build", "link", "run", "test"))
    depends_on("perl-io-socket-ssl@1.42:", type=("build", "run", "test"))
    depends_on("perl-json-maybexs", type=("build", "run", "test"))
    depends_on("perl-lwp-protocol-https", type=("build", "test"))
    depends_on("perl-moo", type=("build", "run", "test"))
    depends_on("perl-net-ssleay@1.49:", type=("build", "run", "test"))
    depends_on("perl-ref-util", type=("build", "run", "test"))
    depends_on("perl-safe-isa", type=("build", "run", "test"))
    depends_on("perl-test-fatal", type=("build", "test"))
    depends_on("perl-test-needs@0.002005:", type=("build", "test"))
    depends_on("perl-type-tiny", type=("build", "run", "test"))
    depends_on("perl-uri", type=("build", "run", "test"))
