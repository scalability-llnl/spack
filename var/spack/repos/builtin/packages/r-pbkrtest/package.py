# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPbkrtest(RPackage):
    """Test in mixed effects models. Attention is on mixed effects models as
    implemented in the 'lme4' package. This package implements a parametric
    bootstrap test and a Kenward Roger modification of F-tests for linear mixed
    effects models and a parametric bootstrap test for generalized linear mixed
    models."""

    homepage = "http://people.math.aau.dk/~sorenh/software/pbkrtest/"
    url      = "https://cloud.r-project.org/src/contrib/pbkrtest_0.4-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pbkrtest"

    version('0.4-7', sha256='5cbb03ad2b2468720a5a610a0ebda48ac08119a34fca77810a85f554225c23ea')
    version('0.4-6', sha256='9d28b8916fea3ffec8d5958bb8c531279b1e273f21fdbeb2fcad6d7e300a9c01')
    version('0.4-4', sha256='a685392ef3fca0ddc2254f6cc9bba6bc22b298fa823359fc4515e64e753abd31')

    depends_on('r@3.0.2:', when='@:0.4-5', type=('build', 'run'))
    depends_on('r@3.2.3:', when='@0.4-6:', type=('build', 'run'))
    depends_on('r-lme4@1.1.10:', type=('build', 'run'))
    depends_on('r-matrix@1.2.3:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
