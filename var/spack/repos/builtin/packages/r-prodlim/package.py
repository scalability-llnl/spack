# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProdlim(RPackage):
    """Product-Limit Estimation for Censored Event History Analysis. Fast and
    user friendly implementation of nonparametric estimators for censored event
    history (survival) analysis. Kaplan-Meier and Aalen-Johansen method."""

    homepage = "https://cloud.r-project.org/package=prodlim"
    url      = "https://cloud.r-project.org/src/contrib/prodlim_1.5.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/prodlim"

    version('2018.04.18', sha256='4b22b54fdf712439309be0ff74f63cde9080464667b00e19823372ac0fc254ab')
    version('1.6.1', sha256='3f2665257118a3db8682731a500b1ae4d669af344672dc2037f987bee3cca154')
    version('1.5.9', sha256='853644886c57102e7f6dd26b6e03e54bf3f9e126f54c76f8d63a3324811f7b42')

    depends_on('r@2.9.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.11.5:', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-kernsmooth', type=('build', 'run'))
    depends_on('r-lava', type=('build', 'run'))
