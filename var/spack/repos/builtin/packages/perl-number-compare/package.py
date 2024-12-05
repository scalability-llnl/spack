# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNumberCompare(PerlPackage):
    """Number::Compare - numeric comparisons"""

    homepage = "https://metacpan.org/pod/Number::Compare"
    url = "https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/Number-Compare-0.03.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.03", sha256="83293737e803b43112830443fb5208ec5208a2e6ea512ed54ef8e4dd2b880827")

    depends_on("perl-extutils-makemaker", type="build")
