# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHashMoreutils(PerlPackage):
    """Provide the stuff missing in Hash::Util"""

    homepage = "https://metacpan.org/pod/Hash::MoreUtils"
    url = "https://cpan.metacpan.org/authors/id/R/RE/REHSACK/Hash-MoreUtils-0.06.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.06", sha256="db9a8fb867d50753c380889a5e54075651b5e08c9b3b721cb7220c0883547de8")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
