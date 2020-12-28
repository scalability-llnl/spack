# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openslide(AutotoolsPackage):
    """OpenSlide reads whole slide image files."""

    homepage = "http://openslide.org/"
    url      = "https://github.com/openslide/openslide/releases/download/v3.4.1/openslide-3.4.1.tar.xz"

    version('3.4.1', sha256='9938034dba7f48fadc90a2cdf8cfe94c5613b04098d1348a5ff19da95b990564')

    depends_on('openjpeg')
    depends_on('jpeg')
    depends_on('libtiff')
    depends_on('libxml2')
    depends_on('sqlite@3.6:')
    depends_on('glib')
    depends_on('cairo+pdf')
    depends_on('gdk-pixbuf')
