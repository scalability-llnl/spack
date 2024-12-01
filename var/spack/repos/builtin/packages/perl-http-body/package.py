# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpBody(PerlPackage):
    """HTTP Body Parser"""

    homepage = "https://metacpan.org/pod/HTTP::Body"
    url = "https://cpan.metacpan.org/authors/id/G/GE/GETTY/HTTP-Body-1.22.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.22", sha256="fc0d2c585b3bd1532d92609965d589e0c87cd380e7cca42fb9ad0a1311227297")

    depends_on("perl-http-message", type=("build", "link", "run", "test"))
    depends_on("perl-test-deep", type=("build", "link"))
