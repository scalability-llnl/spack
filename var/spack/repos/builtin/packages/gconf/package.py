# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gconf(AutotoolsPackage):
    """GConf is a system for storing application preferences."""

    homepage = "https://projects.gnome.org/gconf/"
    url      = "http://ftp.gnome.org/pub/gnome/sources/GConf/3.2/GConf-3.2.6.tar.xz"

    version('3.2.6', sha256='1912b91803ab09a5eed34d364bf09fe3a2a9c96751fde03a4e0cfa51a04d784c')

    depends_on('pkgconfig', type='build')
    depends_on('glib@2.14.0:')
    depends_on('libxml2')
    depends_on('dbus')
    depends_on('dbus-glib')
    depends_on('orbit2')
    depends_on('perl-xml-parser', type=('build', 'run'))
