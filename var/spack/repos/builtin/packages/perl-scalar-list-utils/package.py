# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlScalarListUtils(PerlPackage):
    """Scalar::Util - A selection of general-utility scalar subroutines"""

    homepage = "https://metacpan.org/pod/Scalar::Util"
    url      = "https://cpan.metacpan.org/authors/id/P/PE/PEVANS/Scalar-List-Utils-1.50.tar.gz"

    version('1.50', sha256='06aab9c693380190e53be09be7daed20c5d6278f71956989c24cca7782013675')
