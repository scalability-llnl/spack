# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMockConfig(PerlPackage):
    """Temporarily set Config or XSConfig values"""

    homepage = "https://metacpan.org/pod/Mock::Config"
    url = "https://cpan.metacpan.org/authors/id/R/RU/RURBAN/Mock-Config-0.03.tar.gz"

    maintainers("EbiArnie")

    version("0.03", sha256="a5b8345757ca4f2b9335f5be14e93ebbb502865233a755bf53bc7156deec001b")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
