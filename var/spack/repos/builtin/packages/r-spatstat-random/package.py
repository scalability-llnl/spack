# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatstatRandom(RPackage):
    """Random Generation Functionality for the 'spatstat' Family.

    Functionality for random generation of spatial data in the 'spatstat'
    family of packages. Generates random spatial patterns of points according
    to many simple rules (complete spatial randomness, Poisson, binomial,
    random grid, systematic, cell), randomised alteration of patterns
    (thinning, random shift, jittering), simulated realisations of random point
    processes (simple sequential inhibition, Matern inhibition models, Matern
    cluster process, Neyman-Scott cluster processes, log-Gaussian Cox
    processes, product shot noise cluster processes) and simulation of Gibbs
    point processes (Metropolis-Hastings birth-death-shift algorithm,
    alternating Gibbs sampler). Also generates random spatial patterns of line
    segments, random tessellations, and random images (random noise, random
    mosaics). Excludes random generation on a linear network, which is covered
    by the separate package 'spatstat.linnet'."""

    cran = "spatstat.random"

    version("3.3-1", sha256="83026bce8802e14423edfa0a0f9c8279ef74565992bdac1804dfec357988bbd3")
    version("3.1-4", sha256="a6cd75e187a992fd8dae535f6745e12801635a344ca51bd2fe048debea3df7d3")
    version("3.0-1", sha256="938c845c063b8781bf894c0a67537e7b2a7c425a4beba4a95ec9d2c37b43e5b6")
    version("2.2-0", sha256="45f0bbdb9dbd53b6c4151c3cdd098451cf787729717ccbb063cd1f33910e604d")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-spatstat-data@2.1-0:", type=("build", "run"))
    depends_on("r-spatstat-data@2.2-0.003:", type=("build", "run"), when="@3.0-1:")
    depends_on("r-spatstat-data@3.0:", type=("build", "run"), when="@3.1-4:")
    depends_on("r-spatstat-data@3.1:", type=("build", "run"), when="@3.3-0:")
    depends_on("r-spatstat-geom@2.4-0:", type=("build", "run"))
    depends_on("r-spatstat-geom@2.4-0.023:", type=("build", "run"), when="@3.0-1:")
    depends_on("r-spatstat-geom@3.0-5:", type=("build", "run"), when="@3.1-4:")
    depends_on("r-spatstat-geom@3.3-0:", type=("build", "run"), when="@3.3-0:")
    depends_on("r-spatstat-univar@3.0-0:", type=("build", "run"), when="@3.3-0:")
    depends_on("r-spatstat-utils@2.2-0:", type=("build", "run"))
    depends_on("r-spatstat-utils@2.3-1.003:", type=("build", "run"), when="@3.0-1:")
    depends_on("r-spatstat-utils@3.0-2:", type=("build", "run"), when="@3.1-4:")
    depends_on("r-spatstat-utils@3.0-5:", type=("build", "run"), when="@3.3-0:")
