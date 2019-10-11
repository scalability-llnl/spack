# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


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
    version('2.2.3', md5='a67bd15fa33d4aac0a1c7904aed19f49')
    version('2.1.1', md5='e91a1a99903e460e7ba00a794e72cc1e')

    # Build dependencies
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('gettext', type='build')
    depends_on('pkgconfig', type='build')

    depends_on('libiconv')
    depends_on('libpng')
    depends_on('jpeg')
    depends_on('libtiff')
    depends_on('fontconfig')
