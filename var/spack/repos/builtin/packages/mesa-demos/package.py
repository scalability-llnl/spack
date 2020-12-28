# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MesaDemos(AutotoolsPackage):
    """This package provides some demo applications for testing Mesa."""

    homepage = "http://www.mesa3d.org"
    url      = "https://github.com/freedesktop/mesa-demos/archive/mesa-demos-8.3.0.tar.gz"

    version('8.3.0', sha256='9bc1b37f4fc7bfc3f818f2d3851ffde28e8167ef11dca87f4781e9ef6206901f')
    version('8.2.0', sha256='5a9f71b815d968d0c3b77edfcc3782d0211f8520b00da9e554ccfed80c8889f6')
    version('8.1.0', sha256='cc5826105355830208c90047fc38c5b09fa3ab0045366e7e859104935b00b76d')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('pkgconfig', type='build')
    depends_on('mesa')
    depends_on('mesa-glu')
    depends_on('freetype')
    depends_on('freeglut')
    depends_on('glew@1.5.4:')
