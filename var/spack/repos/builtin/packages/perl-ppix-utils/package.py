# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPpixUtils(PerlPackage):
    """Utility functions for PPI"""

    homepage = "https://metacpan.org/pod/PPIx::Utils"
    url = "https://cpan.metacpan.org/authors/id/D/DB/DBOOK/PPIx-Utils-0.003.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.003", sha256="2a9bccfc8ead03be01b67248fe8e152522040f798286fa4ef4432b7f2efdba11")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-b-keywords@1.09:", type=("build", "run", "test"))
    depends_on("perl-ppi@1.250:", type=("build", "run", "test"))
