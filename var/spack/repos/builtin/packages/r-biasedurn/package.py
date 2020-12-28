# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiasedurn(RPackage):
    """Statistical models of biased sampling in the form of univariate and
       multivariate noncentral hypergeometric distributions, including
       Wallenius' noncentral hypergeometric distribution and Fisher's
       noncentral hypergeometric distribution (also called extended
       hypergeometric distribution). See vignette("UrnTheory") for
       explanation of these distributions."""

    homepage = "http://www.agner.org/random/"
    url      = "https://cloud.r-project.org/src/contrib/BiasedUrn_1.07.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/BiasedUrn/"

    version('1.07', sha256='2377c2e59d68e758a566452d7e07e88663ae61a182b9ee455d8b4269dda3228e')
