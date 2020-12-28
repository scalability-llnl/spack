# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBoot(RPackage):
    """Functions and datasets for bootstrapping from the book "Bootstrap
    Methods and Their Application" by A. C. Davison and D. V. Hinkley (1997,
    CUP), originally written by Angelo Canty for S."""

    homepage = "https://cloud.r-project.org/package=boot"
    url      = "https://cloud.r-project.org/src/contrib/boot_1.3-18.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/boot"

    version('1.3-23', sha256='79236a5a770dc8bf5ce25d9aa303c5dc0574d94aa043fd00b8b4c8ccc877357f')
    version('1.3-22', sha256='cf1f0cb1e0a7a36dcb6ae038f5d0211a0e7a009c149bc9d21acb9c58c38b4dfc')
    version('1.3-20', sha256='adcb90b72409705e3f9c69ea6c15673dcb649b464fed06723fe0930beac5212a')
    version('1.3-18', sha256='12fd237f810a69cc8d0a51a67c57eaf9506bf0341c764f8ab7c1feb73722235e')

    depends_on('r@3.0.0:', type=('build', 'run'))
