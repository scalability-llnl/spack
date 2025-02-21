# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSplancs(RPackage):
    """Spatial and Space-Time Point Pattern Analysis.

    The Splancs package was written as an enhancement to S-Plus for display and
    analysis of spatial point pattern data; it has been ported to R and is in
    "maintenance mode"."""

    cran = "splancs"

    license("GPL-2.0-or-later")

    version("2.01-45", sha256="8bccf1d61d7feaab52da07a9c95aa66bcd3986a6b214f13b232c1e2bea4b76d3")
    version("2.01-43", sha256="b351565e1f69f6c86a29d921d3a18d5896c4586e2ab8c73bb3df8e75630fc448")
    version("2.01-42", sha256="8c0af4764521e20b629dba6afd5c284e7be48786f378c37668eacfa26d2ef0aa")
    version("2.01-40", sha256="79744381ebc4a361740a36dca3c9fca9ae015cfe0bd585b7856a664a3da74363")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-sp@0.9:", type=("build", "run"))
