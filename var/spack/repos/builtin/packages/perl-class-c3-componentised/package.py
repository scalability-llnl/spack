# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClassC3Componentised(PerlPackage):
    """Load mix-ins or components to your C3-based class"""

    homepage = "https://metacpan.org/pod/Class::C3::Componentised"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Class-C3-Componentised-1.001002.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.001002", sha256="3051b146dc1efeaea1a9a2e9e6b1773080995b898ab583f155658d5fc80b9693")

    depends_on("perl@5.6.2:", type=("build", "link", "run", "test"))
    depends_on("perl-class-c3@0.20:", type=("build", "run", "test"))
    depends_on("perl-class-inspector@1.32:", type=("build", "run", "test"))
    depends_on("perl-mro-compat@0.09:", type=("build", "run", "test"))
    depends_on("perl-test-exception@0.31:", type=("build", "test"))
