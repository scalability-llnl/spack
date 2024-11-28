# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDataVisitor(PerlPackage):
    """Visitor style traversal of Perl data structures"""

    homepage = "https://metacpan.org/pod/Data::Visitor"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Data-Visitor-0.32.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.32", sha256="b194290f257cc6275a039374111554c666a1650e4c01ad799c1e0a277f47917d")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-moose@0.89:", type=("build", "run", "test"))
    depends_on("perl-namespace-clean@0.19:", type=("build", "run", "test"))
    depends_on("perl-test-needs", type=("build", "test"))
    depends_on("perl-tie-toobject@0.01:", type=("build", "run", "test"))
