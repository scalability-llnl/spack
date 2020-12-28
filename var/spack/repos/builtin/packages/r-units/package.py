# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUnits(RPackage):
    """Support for measurement units in R vectors, matrices and arrays:
       automatic propagation, conversion, derivation and simplification of
       units; raising errors in case of unit incompatibility. Compatible with
       the POSIXct, Date and difftime classes. Uses the UNIDATA udunits
       library and unit database for unit compatibility checking and
       conversion."""

    homepage = "https://github.com/edzer/units/"
    url      = "https://cloud.r-project.org/src/contrib/units_0.4-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/units"

    version('0.6-3', sha256='03de88d9dcfe80d22dd3813413f33657c576aed24a8091dbfc7f68602020a64f')
    version('0.6-2', sha256='5e286775d0712c8e15b6ae3a533d4c4349b0f6410c2d9d897ca519c3d0e5f170')
    version('0.4-6', sha256='db383c9b7ec221a5da29a2ddf4f74f9064c44ea2102ea7e07cc1cc5bb30fa1ef')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r-udunits2@0.13:', when='@:0.5-1', type=('build', 'run'))
    depends_on('r-rcpp@0.12.10:', type=('build', 'run'))
    depends_on('udunits', when='@0.6-0:')
