# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestDiaginc(PerlPackage):
    """List modules and versions loaded if tests fail"""

    homepage = "https://metacpan.org/pod/Test::DiagINC"
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Test-DiagINC-0.010.tar.gz"

    maintainers("EbiArnie")

    license("Apache-2.0")

    version("0.010", sha256="5bcb8d356c509e359d53d869c07efdaa8fee5d6cf99897018b9a914ceb21222e")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-capture-tiny@0.21:", type=("build", "test"))
