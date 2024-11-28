# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestSharedfork(PerlPackage):
    """Fork test"""

    homepage = "https://metacpan.org/pod/Test::SharedFork"
    url = "https://cpan.metacpan.org/authors/id/E/EX/EXODIST/Test-SharedFork-0.35.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.35", sha256="2932e865610e80758f764c586757ef8e11db1284d958e25e4b7a85098414c59f")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-test-requires", type=("test"))
