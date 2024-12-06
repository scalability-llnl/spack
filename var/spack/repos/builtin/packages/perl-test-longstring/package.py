# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestLongstring(PerlPackage):
    """Tests strings for equality, with more helpful failures"""

    homepage = "https://metacpan.org/pod/Test::LongString"
    url = "https://cpan.metacpan.org/authors/id/R/RG/RGARCIA/Test-LongString-0.17.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.17", sha256="abc4349eaf04d1bec1e464166a3018591ea846d8f3c5c9c8af4ac4905d3e974f")
