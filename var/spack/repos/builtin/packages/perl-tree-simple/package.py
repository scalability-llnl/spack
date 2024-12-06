# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTreeSimple(PerlPackage):
    """A simple tree object"""

    homepage = "https://metacpan.org/pod/Tree::Simple"
    url = "https://cpan.metacpan.org/authors/id/R/RS/RSAVAGE/Tree-Simple-1.34.tgz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.34", sha256="b7e9799bd222bb94cff993f7d765980cbea1b6cd2aaa5ecbead635abdf47d29c")

    depends_on("perl-test-exception@0.15:", type=("build", "test"))
