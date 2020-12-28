# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RColorspace(RPackage):
    """Carries out mapping between assorted color spaces including RGB, HSV,
    HLS, CIEXYZ, CIELUV, HCL (polar CIELUV), CIELAB and polar CIELAB.
    Qualitative, sequential, and diverging color palettes based on HCL colors
    are provided."""

    homepage = "https://cloud.r-project.org/package=colorspace"
    url      = "https://cloud.r-project.org/src/contrib/colorspace_1.3-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/colorspace"

    version('1.4-1', sha256='693d713a050f8bfecdb7322739f04b40d99b55aed168803686e43401d5f0d673')
    version('1.4-0', sha256='ce003c5958dd704697959e9dc8a108c8cb568f8d78ece113235732afc5dff556')
    version('1.3-2', sha256='dd9fd2342b650456901d014e7ff6d2e201f8bec0b555be63b1a878d2e1513e34')
    version('1.2-6', sha256='ba3165c5b906edadcd1c37cad0ef58f780b0af651f3fdeb49fbb2dc825251679')

    depends_on('r@3.0.0:', type=('build', 'run'))
