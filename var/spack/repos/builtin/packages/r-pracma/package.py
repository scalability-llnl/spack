# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPracma(RPackage):
    """Practical Numerical Math Functions.

    Provides a large number of functions from numerical analysis and linear
    algebra, numerical optimization, differential equations, time series, plus
    some well-known special mathematical functions. Uses 'MATLAB' function
    names where appropriate to simplify porting."""

    cran = "pracma"

    license("GPL-3.0-or-later")

    version("2.4.4", sha256="1a4ef3af2197f999dbaa614bf5a70f09ec463d8c91feb5aa0d995de24ec6ba7f")
    version("2.4.2", sha256="1d50337fdfd9a8d704a64f01dae5d52b9a2bd6d872fdaa4a6685b8d3bde89c16")
    version("2.3.8", sha256="2302d454406e72711714732658d0c59c9d5a1ead698f22ee23f38cba63d42764")
    version("2.3.6", sha256="17ac83fd48c9155e00dc3f0433f95723505dc73d046860afd9001866d699b8de")
    version("2.2.9", sha256="0cea0ff5e88643df121e07b9aebfe57084c61e11801680039752f371fe87bf1e")

    depends_on("r@3.1.0:", type=("build", "run"))
