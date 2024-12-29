# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTimedate(PerlPackage):
    """The parser contained here will only parse absolute dates, if you want a
    date parser that can parse relative dates then take a look at the Time
    modules by David Muir on CPAN."""

    homepage = "https://metacpan.org/release/TimeDate"
    url = "https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/TimeDate-2.33.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.33", sha256="c0b69c4b039de6f501b0d9f13ec58c86b040c1f7e9b27ef249651c143d605eb2")
    version("2.30", sha256="75bd254871cb5853a6aa0403ac0be270cdd75c9d1b6639f18ecba63c15298e86")

    def url_for_version(self, version):
        if self.spec.satisfies("@2.31:"):
            return f"https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/TimeDate-{version}.tar.gz"
        else:
            return f"https://cpan.metacpan.org/authors/id/G/GB/GBARR/TimeDate-{version}.tar.gz"
