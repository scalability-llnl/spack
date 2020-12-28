# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rgb(AutotoolsPackage, XorgPackage):
    """X color name database.

    This package includes both the list mapping X color names to RGB values
    (rgb.txt) and, if configured to use a database for color lookup, the
    rgb program to convert the text file into the binary database format.

    The "others" subdirectory contains some alternate color databases."""

    homepage = "http://cgit.freedesktop.org/xorg/app/rgb"
    xorg_mirror_path = "app/rgb-1.0.6.tar.gz"

    version('1.0.6', sha256='cb998035e08b9f58ad3150cab60461c3225bdd075238cffc665e24da40718933')

    depends_on('xorg-server')

    depends_on('xproto', type='build')
