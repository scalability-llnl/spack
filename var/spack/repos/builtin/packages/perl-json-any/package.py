# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlJsonAny(PerlPackage):
    """(DEPRECATED) Wrapper Class for the various JSON classes"""

    homepage = "https://metacpan.org/pod/JSON::Any"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/JSON-Any-1.40.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.40", sha256="083256255a48094fd9ac1239e0fea8a10a2383a9cd1ef4b1c7264ede1b4400ab")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
    depends_on("perl-test-fatal", type=("build", "test"))
    depends_on("perl-test-needs", type=("build", "test"))
    depends_on("perl-test-warnings@0.009:", type=("build", "test"))
    depends_on("perl-test-without-module", type=("build", "test"))
