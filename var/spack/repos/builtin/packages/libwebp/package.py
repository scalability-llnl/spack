# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libwebp(AutotoolsPackage):
    """WebP is a modern image format that provides superior lossless and lossy
    compression for images on the web. Using WebP, webmasters and web
    developers can create smaller, richer images that make the web faster."""

    homepage = "https://developers.google.com/speed/webp/"
    url      = "https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.0.3.tar.gz"

    version('1.0.3', sha256='e20a07865c8697bba00aebccc6f54912d6bc333bb4d604e6b07491c1a226b34f')

    variant('libwebpmux',     default=False, description='Build libwebpmux')
    variant('libwebpdemux',   default=False, description='Build libwebpdemux')
    variant('libwebpdecoder', default=False, description='Build libwebpdecoder')
    variant('libwebpextras',  default=False, description='Build libwebpextras')

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    def configure_args(self):
        # TODO: add variants and dependencies for these
        args = [
            '--disable-gl',
            '--disable-sdl',
            '--disable-png',
            '--disable-jpeg',
            '--disable-tiff',
            '--disable-gif',
            '--disable-wic',
        ]

        if '+libwebpmux' in self.spec:
            args.append('--enable-libwebpmux')
        else:
            args.append('--disable-libwebpmux')

        if '+libwebpdemux' in self.spec:
            args.append('--enable-libwebpdemux')
        else:
            args.append('--disable-libwebpdemux')

        if '+libwebpdecoder' in self.spec:
            args.append('--enable-libwebpdecoder')
        else:
            args.append('--disable-libwebpdecoder')

        if '+libwebpextras' in self.spec:
            args.append('--enable-libwebpextras')
        else:
            args.append('--disable-libwebpextras')

        return args
