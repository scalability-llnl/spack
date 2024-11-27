# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestFile(PerlPackage):
    """Test file attributes"""

    homepage = "https://metacpan.org/pod/Test::File"
    url = "https://cpan.metacpan.org/authors/id/B/BD/BDFOY/Test-File-1.993.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-2.0")

    version("1.993", sha256="ef2ffe1aaec7b42d874ad411ec647547b9b9bc2f5fb93e49e3399488456afc7a")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
