# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMojolicious(PerlPackage):
    """Real-time web framework"""

    homepage = "https://metacpan.org/pod/Mojolicious"
    url = "https://cpan.metacpan.org/authors/id/S/SR/SRI/Mojolicious-9.35.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-2.0")

    version("9.35", sha256="6a4a446ee07fca7c6db72f5d817540d6833009cb8de7cce4c6fb24a15ee7d46b")

    depends_on("perl@5.16.0:", type=("build", "link", "run", "test"))
