# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDtw(RPackage):
    """A comprehensive implementation of dynamic time warping (DTW) algorithms
    in R. DTW computes the optimal (least cumulative distance) alignment
    between points of two time series."""

    homepage = "https://cloud.r-project.org/package=dtw"
    url      = "https://cloud.r-project.org/src/contrib/dtw_1.18-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/dtw"

    version('1.20-1', sha256='43ca1a47a7c81a2b5d5054da1be8b8af79a85d6f9ce7b4512e9ed91f790f60f0')
    version('1.18-1', sha256='d9dab25bdf61705f9f28dc5ca1c96a7465b269233e878516c52c01b5a0da21ad')
    version('1.17-1', sha256='0fc3afcebc58135c78abd7545a3549466ac051a058f913db16214c12141a6e4d')
    version('1.16',   sha256='7d7e34c41ff6021991bcf8a913b2b6b82680018f65fdd90af2150a07457e9cdb')
    version('1.15',   sha256='28ba2110d4c305f332fad93337cdae24b9de4163b8ddf33d476f9dddc63160f1')
    version('1.14-3', sha256='6989358d8d97428418c2b34ae38647efcee2e0ce095800a657d5d83d7083c9e3')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-proxy', type=('build', 'run'))
