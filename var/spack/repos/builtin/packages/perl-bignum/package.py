# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlBignum(PerlPackage):
    """bigint/bigrat/bignum - transparent big number support"""

    homepage = "https://github.com/pjacklam/p5-bignum"
    url = "https://cpan.metacpan.org/authors/id/P/PJ/PJACKLAM/bignum-0.66.tar.gz"

    version("0.67", sha256="1c9a824ab323e3e58d9808011c10ad27589dba1202806278215012ca7f522875")
    version("0.66", sha256="26d48fb4b63a4b738ab84b577f9de7cdec164fe5f8a7089010a1ec17e127ed97")

    depends_on("perl@5.6.0:", type=("build", "run"))
    depends_on("perl-math-bigrat", type=("build", "run"))
    depends_on("perl-math-bigint", type=("build", "run"))
    depends_on("perl-extutils-makemaker", type=("build"))
