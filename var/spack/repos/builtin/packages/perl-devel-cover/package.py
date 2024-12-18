# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDevelCover(PerlPackage):
    """Devel::Cover - Perl extension for code coverage metrics"""

    homepage = "https://metacpan.org/pod/Devel::Cover"
    url = "https://cpan.metacpan.org/authors/id/P/PJ/PJCJ/Devel-Cover-1.40.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.42", sha256="cb9c45dee359f3d259856450389df270e2ecea1b49f5f8800fdb972ff50bbebb")
    version("1.40", sha256="26e2f431fbcf7bff3851f352f83b84067c09ff206f40ab975cad8d2bafe711a8")
