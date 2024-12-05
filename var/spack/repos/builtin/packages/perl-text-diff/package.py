# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTextDiff(PerlPackage):
    """Provides a basic set of services akin to the GNU diff utility."""

    homepage = "https://metacpan.org/pod/Text::Diff"
    url = "http://search.cpan.org/CPAN/authors/id/N/NE/NEILB/Text-Diff-1.45.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.45", sha256="e8baa07b1b3f53e00af3636898bbf73aec9a0ff38f94536ede1dbe96ef086f04")

    depends_on("perl-algorithm-diff", type=("build", "run"))
