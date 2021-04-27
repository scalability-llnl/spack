# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RPartykit(RPackage):
    """A Toolkit for Recursive Partytioning

    A toolkit with infrastructure for representing, summarizing, and
    visualizing tree-structured regression and classification models. This
    unified infrastructure can be used for reading/coercing tree models from
    different sources ('rpart', 'RWeka', 'PMML') yielding objects that share
    functionality for print()/plot()/predict() methods. Furthermore, new and
    improved reimplementations of conditional inference trees (ctree()) and
    model-based recursive partitioning (mob()) from the 'party' package are
    provided based on the new infrastructure. A description of this package was
    published by Hothorn and Zeileis (2015)
    <https://jmlr.org/papers/v16/hothorn15a.html>."""

    homepage = "http://partykit.r-forge.r-project.org/partykit"
    url      = "https://cloud.r-project.org/src/contrib/partykit_1.1-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/partykit"

    version('1.2-11', sha256='3a83332d782a235cfb5ba60cc8f1c51d46ca5477b22979a614f514d1c951c602')
    version('1.2-5', sha256='f48e30790f93fa5d03e68e8ce71ce33d009d107d46d45d85da2016b38b27629c')
    version('1.2-3', sha256='56749b246e283f94ac2ad2cdcfc0a477e05cd44b5e8f6e462c26f4dff818da35')
    version('1.1-1', sha256='d9f4762690cd85ee4e3dc44f5a14069d10a1900afdfbcdc284d2a94b4a8e8332')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@1.2-11:', type=('build', 'run'))
    depends_on('r-libcoin@1.0-0:', when='@1.2-0:', type=('build', 'run'))
    depends_on('r-mvtnorm', when='@1.2-0:', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-formula@1.2-1:', type=('build', 'run'))
    depends_on('r-inum@1.0-0:', when='@1.2-0:', type=('build', 'run'))
    depends_on('r-rpart@4.1-11:', when='@1.2-0:', type=('build', 'run'))
