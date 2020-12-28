# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMixtools(RPackage):
    """mixtools: Tools for Analyzing Finite Mixture Models

    Analyzes finite mixture models for various parametric and semiparametric
    settings."""

    homepage = "https://cloud.r-project.org/package=mixtools"
    url      = "https://cloud.r-project.org/src/contrib/mixtools_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mixtools"

    version('1.1.0', sha256='543fd8d8dc8d4b6079ebf491cf97f27d6225e1a6e65d8fd48553ada23ba88d8f')
    version('1.0.4', sha256='62f4b0a17ce520c4f8ed50ab44f120e459143b461a9e420cd39056ee4fc8798c')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-segmented', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
