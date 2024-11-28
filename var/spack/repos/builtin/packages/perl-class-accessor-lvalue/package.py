# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClassAccessorLvalue(PerlPackage):
    """Create Lvalue accessors"""

    homepage = "https://metacpan.org/pod/Class::Accessor::Lvalue"
    url = "https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/Class-Accessor-Lvalue-0.11.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.11", sha256="ea5b1bcfbc1c3c63004eb280a5415f7dad2a82257675ab033382814fe168913c")

    depends_on("perl-class-accessor", type=("build", "run", "test"))
    depends_on("perl-want", type=("build", "run", "test"))
