# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTimeHires(PerlPackage):
    """High resolution alarm, sleep, gettimeofday, interval timers"""

    homepage = "https://metacpan.org/pod/Time::HiRes"
    url = "http://search.cpan.org/CPAN/authors/id/J/JH/JHI/Time-HiRes-1.9746.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.9758", sha256="5bfa145bc11e70a8e337543b1084a293743a690691b568493455dedf58f34b1e")
    version("1.9746", sha256="89408c81bb827bc908c98eec50071e6e1158f38fa462865ecc3dc03aebf5f596")
