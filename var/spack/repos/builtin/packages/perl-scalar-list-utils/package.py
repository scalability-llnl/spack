# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlScalarListUtils(PerlPackage):
    """Scalar::Util - A selection of general-utility scalar subroutines"""

    homepage = "https://metacpan.org/pod/Scalar::Util"
    url = "https://cpan.metacpan.org/authors/id/P/PE/PEVANS/Scalar-List-Utils-1.50.tar.gz"

    version("1.63", sha256="cafbdf212f6827dc9a0dd3b57b6ee50e860586d7198228a33262d55c559eb2a9")
    version("1.50", sha256="06aab9c693380190e53be09be7daed20c5d6278f71956989c24cca7782013675")
