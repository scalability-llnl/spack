# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openblas(Package):
    """OpenBLAS: An optimized BLAS library"""
    homepage = "http://www.openblas.net"
    url      = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version('0.2.15', 'b1190f3d3471685f17cfd1ec1d252ac9')
    version('0.2.14', 'b1190f3d3471685f17cfd1ec1d252ac9')
    version('0.2.13', 'b1190f3d3471685f17cfd1ec1d252ac9')

    # See #20019 for this conflict
    conflicts('%gcc@:4.4.99', when='@0.2.14:')

    provides('blas')
