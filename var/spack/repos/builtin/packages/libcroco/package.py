# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcroco(AutotoolsPackage):
    """Libcroco is a standalone css2 parsing and manipulation library."""

    homepage = "https://developer.gnome.org/libcroco"
    url      = "http://ftp.gnome.org/pub/gnome/sources/libcroco/0.6/libcroco-0.6.12.tar.xz"

    version('0.6.12', sha256='ddc4b5546c9fb4280a5017e2707fbd4839034ed1aba5b7d4372212f34f84f860')

    depends_on('glib')
    depends_on('libxml2')
    depends_on('pkgconfig', type='build')
