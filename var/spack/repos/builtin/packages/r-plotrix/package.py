# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPlotrix(RPackage):
    """Lots of plots, various labeling, axis and color scaling functions."""

    homepage = "https://cloud.r-project.org/package=plotrix"
    url      = "https://cloud.r-project.org/src/contrib/plotrix_3.6-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/plotrix"

    version('3.7-6', sha256='83d5f7574592953288b4fe39c4c0dd7670d097598ad7f6bddbb0687a32954e46')
    version('3.7-5', sha256='b22f3f9d93961d23ad46e41597d1e45d2665ced04dcad8c40f6806a67cded14c')
    version('3.6-4', sha256='883b7d0a00c1b2b418f9167c72ed9e86eca3c9865d34158a7a6ad0b9bf95bff3')
    version('3.6-3', sha256='217164bdd04405c3280a0c8b2691f289287f9851fa8248648a5ae38f54962741')

    depends_on('r@3.5.0:', when='@3.7-6:', type=('build', 'run'))
