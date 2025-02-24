# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNor1mix(RPackage):
    """Normal aka Gaussian (1-d) Mixture Models (S3 Classes and Methods).

    One dimensional Normal Mixture Models Classes, for, e.g., density
    estimation or clustering algorithms research and teaching; providing the
    widely used Marron-Wand densities. Efficient random number generation and
    graphics; now fitting to data by ML (Maximum Likelihood) or EM
    estimation."""

    cran = "nor1mix"

    license("GPL-2.0-or-later")

    version("1.3-3", sha256="97bfd0f8c847fa68bf607aaa465845a34ac8a7a262315073026a6a1937dd076e")
    version("1.3-0", sha256="9ce4ee92f889a4a4041b5ea1ff09396780785a9f12ac46f40647f74a37e327a0")
    version("1.2-3", sha256="435e6519e832ef5229c51ccb2619640e6b50dfc7470f70f0c938d18a114273af")
