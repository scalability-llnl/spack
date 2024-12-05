# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClassC3(PerlPackage):
    """A pragma to use the C3 method resolution order algorithm"""

    homepage = "https://metacpan.org/pod/Class::C3"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Class-C3-0.35.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.35", sha256="84053cf1a68fcc8c12056c2f120adf04f7f68e3be34f4408e95d026fee67e33e")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-algorithm-c3@0.07:", type=("build", "run", "test"))
