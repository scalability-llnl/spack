# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlJavascriptMinifierXs(PerlPackage):
    """XS based JavaScript minifier"""

    homepage = "https://metacpan.org/pod/JavaScript::Minifier::XS"
    url = "https://cpan.metacpan.org/authors/id/G/GT/GTERMARS/JavaScript-Minifier-XS-0.15.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.15", sha256="5d9b034f58f0b6ff5b64647bd3c5a9ce05b2a70edee339fbc3173aee747cc050")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-test-diaginc@0.002:", type=("build", "test"))
