# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPki(RPackage):
    """Public Key Infrastucture functions such as verifying certificates,
    RSA encription and signing which can be used to build PKI infrastructure
    and perform cryptographic tasks."""

    homepage = "http://www.rforge.net/PKI"
    cran = "PKI"

    license("GPL-2.0-or-later", checked_by="wdconinc")

    version("0.1-14", sha256="c024e81977b978b705460df96639e3369420bd7e8f4f3242ec796255dc1b7966")

    depends_on("r@2.9.0:", type=("build", "run"))
    depends_on("r-base64enc", type=("build", "run"))
