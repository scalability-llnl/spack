# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestRequires(PerlPackage):
    """Checks to see if the module can be loaded."""

    homepage = "https://metacpan.org/pod/Test::Requires"
    url = "http://search.cpan.org/CPAN/authors/id/T/TO/TOKUHIROM/Test-Requires-0.10.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.11", sha256="4b88de549597eecddf7c3c38a4d0204a16f59ad804577b671896ac04e24e040f")
    version("0.10", sha256="2768a391d50ab94b95cefe540b9232d7046c13ee86d01859e04c044903222eb5")
