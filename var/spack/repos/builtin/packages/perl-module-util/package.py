# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleUtil(PerlPackage):
    """Module name tools and transformations"""

    homepage = "https://metacpan.org/pod/Module::Util"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MATTLAW/Module-Util-1.09.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.09", sha256="6cfbcb6a45064446ec8aa0ee1a7dddc420b54469303344187aef84d2c7f3e2c6")

    depends_on("perl@5.5.3:", type=("build", "link", "run", "test"))
