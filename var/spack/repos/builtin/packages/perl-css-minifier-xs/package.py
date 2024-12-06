# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCssMinifierXs(PerlPackage):
    """XS based CSS minifier"""

    homepage = "https://metacpan.org/pod/CSS::Minifier::XS"
    url = "https://cpan.metacpan.org/authors/id/G/GT/GTERMARS/CSS-Minifier-XS-0.13.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.13", sha256="c419e308cdc82af1c25d6b8d07b2ff26347a622b7a63ec20856abe8db4051f82")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-test-diaginc@0.002:", type=("build", "test"))
