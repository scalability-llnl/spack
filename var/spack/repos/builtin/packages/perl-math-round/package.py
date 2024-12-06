# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMathRound(PerlPackage):
    """Math::Round - Perl extension for rounding numbers"""

    homepage = "https://metacpan.org/pod/Math::Round"
    url = "https://cpan.metacpan.org/authors/id/G/GR/GROMMEL/Math-Round-0.07.tar.gz"

    version("0.07", sha256="73a7329a86e54a5c29a440382e5803095b58f33129e61a1df0093b4824de9327")
