# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTreeSimpleVisitorfactory(PerlPackage):
    """A factory object for dispensing Visitor objects"""

    homepage = "https://metacpan.org/pod/Tree::Simple::VisitorFactory"
    url = "https://cpan.metacpan.org/authors/id/R/RS/RSAVAGE/Tree-Simple-VisitorFactory-0.16.tgz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.16", sha256="9cf538faa12c54ffb4a91439945e488f1856f62b89ac5072a922119e01880da6")

    depends_on("perl-test-exception@0.15:", type=("build", "test"))
    depends_on("perl-tree-simple@1.12:", type=("build", "run", "test"))
