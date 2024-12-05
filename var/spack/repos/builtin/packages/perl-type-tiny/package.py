# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTypeTiny(PerlPackage):
    """Tiny, yet Moo(se)-compatible type constraint"""

    homepage = "https://metacpan.org/pod/Type::Tiny"
    url = "https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Type-Tiny-2.004000.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.004000", sha256="697e7f775edfc85f4cf07792d04fd19b09c25285f98f5938e8efc4f74507a128")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-exporter-tiny@1.006000:", type=("run"))
