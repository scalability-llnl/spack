# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpHeadersFast(PerlPackage):
    """Faster implementation of HTTP::Headers"""

    homepage = "https://metacpan.org/pod/HTTP::Headers::Fast"
    url = "https://cpan.metacpan.org/authors/id/T/TO/TOKUHIROM/HTTP-Headers-Fast-0.22.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.22", sha256="cc431db68496dd884db4bc0c0b7112c1f4a4f1dc68c4f5a3caa757a1e7481b48")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-http-date", type=("build", "run", "test"))
    depends_on("perl-module-build-tiny@0.035:", type=("build"))
    depends_on("perl-test-requires", type=("build", "test"))
