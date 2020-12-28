# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNor1mix(RPackage):
    """Onedimensional Normal Mixture Models Classes, for, e.g., density
       estimation or clustering algorithms research and teaching; providing
       the widely used Marron-Wand densities. Efficient random number
       generation and graphics; now fitting to data by ML (Maximum Likelihood)
       or EM estimation."""

    homepage = "https://cloud.r-project.org/package=nor1mix"
    url      = "https://cloud.r-project.org/src/contrib/nor1mix_1.2-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/nor1mix"

    version('1.3-0', sha256='9ce4ee92f889a4a4041b5ea1ff09396780785a9f12ac46f40647f74a37e327a0')
    version('1.2-3', sha256='435e6519e832ef5229c51ccb2619640e6b50dfc7470f70f0c938d18a114273af')
