# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Libvips(AutotoolsPackage):
    """libvips is a demand-driven, horizontally threaded image processing
    library. Compared to similar libraries, libvips runs quickly and uses
    little memory."""

    homepage = "https://libvips.github.io/libvips/"
    url      = "https://github.com/libvips/libvips/releases/download/v8.9.0/vips-8.9.0.tar.gz"
    git      = "https://github.com/libvips/libvips.git"

    version('8.10.5', sha256='a4eef2f5334ab6dbf133cd3c6d6394d5bdb3e76d5ea4d578b02e1bc3d9e1cfd8')
    version('8.9.1',  sha256='45633798877839005016c9d3494e98dee065f5cb9e20f4552d3b315b8e8bce91')
    version('8.9.0',  sha256='97334a5e70aff343d2587f23cb8068fc846a58cd937c89a446142ccf00ea0349')

    variant('fftw', default=True,
            description='Uses FFTW3 for fourier transforms.')

    variant('jpeg', default=False,
            description='Enable JPEG support')

    variant('tiff', default=False,
            description='Enable TIFF support')

    variant('png', default=False,
            description='Enable pngfile support')

    variant('poppler', default=False,
            description='Enable PDF rendering via poppler')

    # TODO: Add more variants!

    depends_on('glib')
    depends_on('expat')

    depends_on('fftw', when='+fftw')
    depends_on('libjpeg', when='+jpeg')
    depends_on('libtiff', when='+tiff')
    depends_on('libpng', when='+png')
    depends_on('poppler', when='+poppler')
