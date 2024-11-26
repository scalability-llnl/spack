# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPackageStashXs(PerlPackage):
    """Faster and more correct implementation of the Package::Stash API"""

    homepage = "https://metacpan.org/pod/Package::Stash::XS"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Package-Stash-XS-0.30.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.30", sha256="26bad65c1959c57379b3e139dc776fbec5f702906617ef27cdc293ddf1239231")
    version("0.28", sha256="23d8c5c25768ef1dc0ce53b975796762df0d6e244445d06e48d794886c32d486")

    def url_for_version(self, version):
        if self.spec.satisfies("@0.29:"):
            return f"https://cpan.metacpan.org/authors/id/E/ET/ETHER/Package-Stash-XS-{version}.tar.gz"
        else:
            return f"http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Package-Stash-XS-{version}.tar.gz"
