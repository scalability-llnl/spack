# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlImportInto(PerlPackage):
    """Import packages into other packages"""

    homepage = "https://metacpan.org/pod/Import::Into"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Import-Into-1.002005.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.002005", sha256="bd9e77a3fb662b40b43b18d3280cd352edf9fad8d94283e518181cc1ce9f0567")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-module-runtime", type=("build", "run", "test"))
