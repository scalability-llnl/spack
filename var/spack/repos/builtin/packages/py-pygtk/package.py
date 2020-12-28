# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygtk(AutotoolsPackage):
    """bindings for the Gtk2 in Python.
       use pygobject for Gtk3."""
    homepage = "http://www.pygtk.org/"
    url      = "http://ftp.gnome.org/pub/GNOME/sources/pygtk/2.24/pygtk-2.24.0.tar.gz"

    version('2.24.0', sha256='6e3e54fa6e65a69ac60bd58cb2e60a57f3346ac52efe995f3d10b6c38c972fd8')

    extends('python')

    depends_on('pkgconfig', type=('build'))
    depends_on("libffi")
    # atk@2.28.1 depends on meson which requires python 3
    depends_on('atk@:2.20.0')
    # PyGTK requires python 2
    # Use py-pygobject@3: for GTK bindings for python 3
    depends_on('python@2:2.99', type=('build', 'run'))
    depends_on('cairo')
    depends_on('glib')
    # for GTK 3.X use pygobject 3.X instead of pygtk
    depends_on('gtkplus@2.24:2.99')
    depends_on('py-pygobject@2.28:2.99', type=('build', 'run'))
    depends_on('py-py2cairo', type=('build', 'run'))

    def install(self, spec, prefix):
        make('install', parallel=False)
