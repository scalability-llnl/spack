# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BppPhyl(CMakePackage):
    """Bio++ phylogeny library."""

    homepage = "http://biopp.univ-montp2.fr/wiki/index.php/Installation"
    url      = "http://biopp.univ-montp2.fr/repos/sources/bpp-phyl-2.2.0.tar.gz"

    version('2.2.0', sha256='f346d87bbc7858924f3c99d7d74eb4a1f7a1b926746c68d8c28e07396c64237b')

    depends_on('cmake@2.6:', type='build')
    depends_on('bpp-core')
    depends_on('bpp-seq')

    # Clarify isnan's namespace, because Fujitsu compiler can't
    # resolve ambiguous of 'isnan' function.
    patch('clarify_isnan.patch', when='%fj')

    def cmake_args(self):
        return ['-DBUILD_TESTING=FALSE']
