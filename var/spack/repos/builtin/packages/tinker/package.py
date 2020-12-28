# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Tinker(CMakePackage):
    """The Tinker molecular modeling software is a complete and general
       package for molecular mechanics and dynamics, with some special
       features for biopolymers.
    """

    homepage = "https://dasher.wustl.edu/tinker/"
    url      = "https://dasher.wustl.edu/tinker/downloads/tinker-8.7.1.tar.gz"

    version('8.7.1', sha256='0d6eff8bbc9be0b37d62b6fd3da35bb5499958eafe67aa9c014c4648c8b46d0f')
    patch('tinker-8.7.1-cmake.patch')

    depends_on('fftw')

    root_cmakelists_dir = 'source'
