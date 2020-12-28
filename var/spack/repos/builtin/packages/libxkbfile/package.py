# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxkbfile(AutotoolsPackage, XorgPackage):
    """XKB file handling routines."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libxkbfile"
    xorg_mirror_path = "lib/libxkbfile-1.0.9.tar.gz"

    version('1.0.9', sha256='95df50570f38e720fb79976f603761ae6eff761613eb56f258c3cb6bab4fd5e3')

    depends_on('libx11')

    depends_on('kbproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
