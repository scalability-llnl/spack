# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlListSomeutils(PerlPackage):
    """Provide the stuff missing in List::Util"""

    homepage = "https://metacpan.org/pod/List::SomeUtils"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/List-SomeUtils-0.59.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.59", sha256="fab30372e4c67bf5a46062da38d1d0c8756279feada866eb439fa29571a2dc7b")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-module-implementation@0.04:", type=("build", "run", "test"))
    depends_on("perl-test-leaktrace", type=("build", "test"))
