# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpCookiejar(PerlPackage):
    """A minimalist HTTP user agent cookie jar"""

    homepage = "https://metacpan.org/pod/HTTP::CookieJar"
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/HTTP-CookieJar-0.014.tar.gz"

    maintainers("EbiArnie")

    license("Apache-2.0")

    version("0.014", sha256="7094ea5c91f536d263b85e83ab4e9a963e11c4408ce08ecae553fa9c0cc47e73")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-http-date", type=("run"))
    depends_on("perl-test-deep", type=("test"))
    depends_on("perl-test-requires", type=("test"))
    depends_on("perl-uri", type=("test"))
