# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHtmlParser(PerlPackage):
    """HTML parser class"""

    homepage = "https://metacpan.org/pod/HTML::Parser"
    url = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/HTML-Parser-3.72.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("3.72", sha256="ec28c7e1d9e67c45eca197077f7cdc41ead1bb4c538c7f02a3296a4bb92f608b")

    depends_on("c", type="build")  # generated

    depends_on("perl-html-tagset", type=("build", "run"))
