# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestFatal(PerlPackage):
    """Incredibly simple helpers for testing code with exceptions"""

    homepage = "https://metacpan.org/pod/Test::Fatal"
    url = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Test-Fatal-0.014.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.017", sha256="37dfffdafb84b762efe96b02fb2aa41f37026c73e6b83590db76229697f3c4a6")
    version("0.014", sha256="bcdcef5c7b2790a187ebca810b0a08221a63256062cfab3c3b98685d91d1cbb0")

    depends_on("perl-try-tiny", type=("build", "run"))
