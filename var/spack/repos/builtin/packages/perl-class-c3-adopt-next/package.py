# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClassC3AdoptNext(PerlPackage):
    """Make NEXT suck less"""

    homepage = "https://metacpan.org/pod/Class::C3::Adopt::NEXT"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Class-C3-Adopt-NEXT-0.14.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.14", sha256="85676225aadb76e8666a6abe2e0659d40eb4581ad6385b170eea4e1d6bf34bf7")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-module-build-tiny@0.039:", type=("build"))
    depends_on("perl-mro-compat", type=("build", "run", "test"))
    depends_on("perl-test-exception@0.27:", type=("build", "test"))
