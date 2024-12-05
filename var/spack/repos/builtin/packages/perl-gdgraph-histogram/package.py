# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlGdgraphHistogram(PerlPackage):
    """GD::Graph::histogram extends the GD::Graph module to create histograms.
    The module allow creation of count or percentage histograms."""

    homepage = "https://metacpan.org/pod/GD::Graph::histogram"
    url = "https://cpan.metacpan.org/authors/id/W/WH/WHIZDOG/GDGraph-histogram-1.1.tar.gz"

    license("Artistic-1.0-cl8")

    version("1.1", sha256="20f752d0e6deb59b29aa2ec3496b5883476d00280b6e83f5b47c33fac4097f8a")
