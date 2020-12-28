# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRngtools(RPackage):
    """This package contains a set of functions for working with Random Number
    Generators (RNGs). In particular, it defines a generic S4 framework for
    getting/setting the current RNG, or RNG data that are embedded into objects
    for reproducibility. Notably, convenient default methods greatly facilitate
    the way current RNG settings can be changed."""

    homepage = "https://renozao.github.io/rngtools"
    url      = "https://cloud.r-project.org/src/contrib/rngtools_1.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rngtools"

    version('1.4', sha256='3aa92366e5d0500537964302f5754a750aff6b169a27611725e7d84552913bce')
    version('1.3.1.1', sha256='99e1a8fde6b81128d0946746c1ef84ec5b6c2973ad843a080098baf73aa3364c')
    version('1.3.1', sha256='763fc493cb821a4d3e514c0dc876d602a692c528e1d67f295dde70c77009e224')

    depends_on('r@3.0.0:', when='@:1.3.1', type=('build', 'run'))
    depends_on('r@3.6.0:', when='@1.3.1.1', type=('build', 'run'))
    depends_on('r@3.2.0:', when='@1.4:', type=('build', 'run'))
    depends_on('r-pkgmaker@0.20:', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
