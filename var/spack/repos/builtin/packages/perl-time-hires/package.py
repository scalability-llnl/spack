# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTimeHires(PerlPackage):
    """High resolution alarm, sleep, gettimeofday, interval timers"""

    homepage = "http://search.cpan.org/~jhi/Time-HiRes-1.9746/HiRes.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/J/JH/JHI/Time-HiRes-1.9746.tar.gz"

    version('1.9746', sha256='89408c81bb827bc908c98eec50071e6e1158f38fa462865ecc3dc03aebf5f596')
