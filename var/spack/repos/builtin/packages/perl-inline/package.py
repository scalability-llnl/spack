# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlInline(PerlPackage):
    """Write Perl Subroutines in Other Programming Languages"""

    homepage = "https://metacpan.org/pod/Inline"
    url = "http://search.cpan.org/CPAN/authors/id/I/IN/INGY/Inline-0.80.tar.gz"

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.86", sha256="510a7de2d011b0db80b0874e8c0f7390010991000ae135cff7474df1e6d51e3a")
    version("0.80", sha256="7e2bd984b1ebd43e336b937896463f2c6cb682c956cbd2c311a464363d2ccef6")

    depends_on("perl-test-warn", type=("build", "run"))
