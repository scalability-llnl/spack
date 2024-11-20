# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileListing(PerlPackage):
    """Parse directory listing"""

    homepage = "https://metacpan.org/pod/File::Listing"
    url = "https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/File-Listing-6.16.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("6.16", sha256="189b3a13fc0a1ba412b9d9ec5901e9e5e444cc746b9f0156d4399370d33655c6")
    version("6.04", sha256="1e0050fcd6789a2179ec0db282bf1e90fb92be35d1171588bd9c47d52d959cf5")

    depends_on("perl-http-date", type=("build", "run"))

    def url_for_version(self, version):
        if self.spec.satisfies("@6.05:"):
            return (
                f"https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/File-Listing-{version}.tar.gz"
            )
        else:
            return (
                f"http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/File-Listing-{version}.tar.gz"
            )
