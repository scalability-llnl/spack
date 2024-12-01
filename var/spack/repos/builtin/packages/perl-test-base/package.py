# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestBase(PerlPackage):
    """A Data Driven Testing Framework"""

    homepage = "https://metacpan.org/pod/Test::Base"
    url = "https://cpan.metacpan.org/authors/id/I/IN/INGY/Test-Base-0.89.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.89", sha256="2794a1aaaeb1d3a287dd2c7286258663796562f7db9ccc6b424bc4f1de8ad014")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-algorithm-diff@1.15:", type=("build", "test"))
    depends_on("perl-spiffy@0.40:", type=("run", "test"))
    depends_on("perl-text-diff@0.35:", type=("build", "test"))
