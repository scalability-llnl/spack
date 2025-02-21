# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCountrycode(RPackage):
    """Convert Country Names and Country Codes.

    Countrycode standardizes country names, converts them into ~40 different
    coding schemes, and assigns region descriptors."""

    cran = "countrycode"

    license("GPL-3.0-only")

    version("1.6.0", sha256="f9db110e32c0bcc90eed85303277660de37a777681bb78e8898b6fc5f2253db6")
    version("1.4.0", sha256="99dfe7652c1e631b9e0f8fac0b0163e7a3fdde8476498555d553e0d1c5fdccc4")
    version("1.3.0", sha256="34361416e771ece1d56dc56f79416c8b7f9591885773becae270684d095bc70f")
    version("1.2.0", sha256="32c65702dcc33d512ff99f14c12f4e0c48fe7ed7c8aa2f0a64194576d129dd40")

    depends_on("r@2.10:", type=("build", "run"))
