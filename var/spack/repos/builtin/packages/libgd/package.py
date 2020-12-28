# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libgd(AutotoolsPackage):
    """GD is an open source code library for the dynamic creation of images
       by programmers. GD is written in C, and "wrappers" are available
       for Perl, PHP and other languages. GD creates PNG, JPEG, GIF,
       WebP, XPM, BMP images, among other formats. GD is commonly used to
       generate charts, graphics, thumbnails, and most anything else, on
       the fly. While not restricted to use on the web, the most common
       applications of GD involve website development.

    """

    homepage = "https://github.com/libgd/libgd"
    url      = 'https://github.com/libgd/libgd/releases/download/gd-2.2.4/libgd-2.2.4.tar.gz'

    version('2.2.4', sha256='487a650aa614217ed08ab1bd1aa5d282f9d379cfd95c756aed0b43406381be65')

    # Build dependencies
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('gettext', type='build')
    depends_on('pkgconfig', type='build')

    depends_on('iconv')
    depends_on('libpng')
    depends_on('jpeg')
    depends_on('libtiff')
    depends_on('fontconfig')

    def patch(self):
        p = self.spec['jpeg'].libs.search_flags
        filter_file(
            'LIBJPEG_LIBS " -ljpeg"',
            'LIBJPEG_LIBS "{0} -ljpeg"'.format(p),
            'configure',
            string=True
        )
