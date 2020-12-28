# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Imlib2(AutotoolsPackage, SourceforgePackage):
    """
    Library that does image file loading and saving as well as rendering,
    manipulation, arbitrary polygon support
    """

    homepage = "http://sourceforge.net/projects/enlightenment/"
    sourceforge_mirror_path = "enlightenment/imlib2-1.5.1.tar.bz2"

    maintainers = ['TheQueasle']

    version('1.6.1', sha256='4d393a77e13da883c8ee2da3b029da3570210fe37d000c9ac33d9fce751b166d')
    version('1.6.0', sha256='cfc440ddfaed5fc85ba2572ad8d87a87cd77a5bffb33ebca882c42cefcd8691d')
    version('1.5.1', sha256='fa4e57452b8843f4a70f70fd435c746ae2ace813250f8c65f977db5d7914baae')

    depends_on('libtiff')
    depends_on('giflib')
    depends_on('bzip2')
    depends_on('freetype')
    depends_on('libxext')
    depends_on('libpng')
    depends_on('libid3tag')
    depends_on('libjpeg-turbo')
