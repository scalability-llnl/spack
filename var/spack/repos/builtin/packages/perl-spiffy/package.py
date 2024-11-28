# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSpiffy(PerlPackage):
    """Spiffy Perl Interface Framework For You"""

    homepage = "https://metacpan.org/pod/Spiffy"
    url = "https://cpan.metacpan.org/authors/id/I/IN/INGY/Spiffy-0.46.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.46", sha256="8f58620a8420255c49b6c43c5ff5802bd25e4f09240c51e5bf2b022833d41da3")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
