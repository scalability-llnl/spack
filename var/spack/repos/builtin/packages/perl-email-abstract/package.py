# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlEmailAbstract(PerlPackage):
    """Unified interface to mail representations"""

    homepage = "https://metacpan.org/pod/Email::Abstract"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Email-Abstract-3.010.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("3.010", sha256="8c12f68b5974cafc99d74942abefc8597193035aafd2763128e6aaafca4b7ed6")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-email-simple@1.998:", type=("build", "run", "test"))
    depends_on("perl-module-pluggable@1.5:", type=("build", "run", "test"))
    depends_on("perl-mro-compat", type=("build", "run", "test"))
