# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMathVecstat(PerlPackage):
    """Math::VecStat - Some basic numeric stats on vectors"""

    homepage = "https://metacpan.org/pod/Math::VecStat"
    url = "https://cpan.metacpan.org/authors/id/A/AS/ASPINELLI/Math-VecStat-0.08.tar.gz"

    version("0.08", sha256="409a8e0e4b1025c8e80f628f65a9778aa77ab285161406ca4a6c097b13656d0d")
