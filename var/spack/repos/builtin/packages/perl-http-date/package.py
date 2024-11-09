# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpDate(PerlPackage):
    """Date conversion routines"""

    homepage = "https://metacpan.org/pod/HTTP::Date"
    url = "https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Date-6.06.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("6.06", sha256="7b685191c6acc3e773d1fc02c95ee1f9fae94f77783175f5e78c181cc92d2b52")
    version("6.02", sha256="e8b9941da0f9f0c9c01068401a5e81341f0e3707d1c754f8e11f42a7e629e333")

    def url_for_version(self, version):
        if self.spec.satisfies("@6.03:"):
            return f"https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Date-{version}.tar.gz"
        else:
            return f"http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/HTTP-Date-{version}.tar.gz"
