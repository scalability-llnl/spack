# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLwpMediatypes(PerlPackage):
    """Guess media type for a file or a URL"""

    homepage = "https://metacpan.org/pod/LWP::MediaTypes"
    url = "https://cpan.metacpan.org/authors/id/O/OA/OALDERS/LWP-MediaTypes-6.04.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("6.04", sha256="8f1bca12dab16a1c2a7c03a49c5e58cce41a6fec9519f0aadfba8dad997919d9")
    version("6.02", sha256="18790b0cc5f0a51468495c3847b16738f785a2d460403595001e0b932e5db676")

    def url_for_version(self, version):
        if self.spec.satisfies("@6.03:"):
            return f"https://cpan.metacpan.org/authors/id/O/OA/OALDERS/LWP-MediaTypes-{version}.tar.gz"
        else:
            return (
                f"http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/LWP-MediaTypes-{version}.tar.gz"
            )
