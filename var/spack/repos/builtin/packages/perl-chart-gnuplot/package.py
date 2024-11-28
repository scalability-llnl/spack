# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlChartGnuplot(PerlPackage):
    """Plot graph using Gnuplot in Perl on the fly"""

    homepage = "https://metacpan.org/pod/Chart::Gnuplot"
    url = "https://cpan.metacpan.org/authors/id/K/KW/KWMAK/Chart/Gnuplot/Chart-Gnuplot-0.23.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.23", sha256="dcb46c0f93436464bdc3403469c828c6c33e954123a2adf4092fbb30bb244b6c")
