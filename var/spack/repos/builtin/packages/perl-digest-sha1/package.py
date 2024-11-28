# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDigestSha1(PerlPackage):
    """Perl interface to the SHA-1 algorithm"""

    homepage = "https://metacpan.org/pod/Digest::SHA1"
    url = "https://cpan.metacpan.org/authors/id/G/GA/GAAS/Digest-SHA1-2.13.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("2.13", sha256="68c1dac2187421f0eb7abf71452a06f190181b8fc4b28ededf5b90296fb943cc")

    depends_on("perl@5.4.0:", type=("build", "link", "run", "test"))
