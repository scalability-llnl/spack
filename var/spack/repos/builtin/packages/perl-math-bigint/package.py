# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMathBigint(PerlPackage):
    """Math::BigInt - arbitrary size integer math package"""

    homepage = "https://metacpan.org/pod/Math::BigInt"
    url = "https://cpan.metacpan.org/authors/id/P/PJ/PJACKLAM/Math-BigInt-1.999837.tar.gz"

    version("2.003002", sha256="5ac1fd255cca29d7cf5cb9283e6bb8177cdb07c5bb97502a58084b1c6eace35c")
    version("1.999838", sha256="d3c2fb37d412ac8d126452caad5764f02193147261b59c56e652167c41d1e9d5")
    version("1.999837", sha256="038f9aad6318f20a84a7b1afe3087a1b02406c9988ce5919311a797f85a32962")
