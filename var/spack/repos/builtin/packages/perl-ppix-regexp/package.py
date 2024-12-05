# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPpixRegexp(PerlPackage):
    """Parse regular expressions"""

    homepage = "https://metacpan.org/pod/PPIx::Regexp"
    url = "https://cpan.metacpan.org/authors/id/W/WY/WYANT/PPIx-Regexp-0.088.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.088", sha256="885433f9b102fad4fd36b21c7320bb036036111caf998131bf416f7cd5ee9764")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-ppi", type=("build", "run", "test"))
    depends_on("perl-task-weaken", type=("build", "run", "test"))
