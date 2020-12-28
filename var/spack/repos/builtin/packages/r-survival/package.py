# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSurvival(RPackage):
    """Contains the core survival analysis routines, including definition of
    Surv objects, Kaplan-Meier and Aalen-Johansen (multi-state) curves, Cox
    models, and parametric accelerated failure time models."""

    homepage = "https://cloud.r-project.org/package=survival"
    url      = "https://cloud.r-project.org/src/contrib/survival_2.41-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/survival"

    version('3.1-12', sha256='b62ed66eb646f3df13f7e9bf6571e3bfecae128c66491e174c8833cbef1bf21f')
    version('2.44-1.1', sha256='55b151e15fcd24ccb3acf60331c9a7ad82bc10f3841ab3be9bc2a37e9ee751b9')
    version('2.44-1', sha256='82c44afa41fe4504295855f1da4a5940c3289dfd61bc664bf211bb67c051a909')
    version('2.41-3', sha256='f3797c344de93abd2ba8c89568770a13524a8b2694144ae55adec46921c8961d')
    version('2.40-1', sha256='91d5217847e39bebcbce4f0a2e295304e5816b1270e71f5f2ed39807f004ee82')
    version('2.39-5', sha256='607170ebe36080d102e884cf13c3b29df01d6bb3b593258afffa67fee2a0ada7')

    depends_on('r@2.13.0:', type=('build', 'run'))
    depends_on('r@3.4:', when='@3.1-12:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
