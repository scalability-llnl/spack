# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMathBigrat(PerlPackage):
    """Math::BigRat - arbitrary size rational number math package"""

    homepage = "https://metacpan.org/pod/Math::BigRat"
    url = "https://cpan.metacpan.org/authors/id/P/PJ/PJACKLAM/Math-BigRat-0.2624.tar.gz"

    version("0.260805", sha256="9e41be24272e262fadc1921c7f51ff218384c92e5628cb53bf62b3026710fd41")

    depends_on("perl@5.6.0:", type=("build", "run"))
    depends_on("perl-module-install", type=("build"))
