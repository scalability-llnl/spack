# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Wayland(AutotoolsPackage):
    """Wayland is a project to define a protocol for a compositor to talk
    to its clients as well as a library implementation of the protocol.
    The compositor can be a standalone display server running on Linux
    kernel modesetting and evdev input devices, an X application, or a
    wayland client itself.  The clients can be traditional applications,
    X servers(rootless or fullscreen) or other display servers."""

    homepage = "http://wayland.freedesktop.org/"
    url      = "https://github.com/wayland-project/wayland/archive/1.18.0.tar.gz"

    version('1.18.0',  sha256='8d375719ebfa36b6f2968096fdf0bfa7d39ba110b7956c0032e395e7e012f332')
    version('1.17.93', sha256='293536ad23bfed15fc34e2a63bbb511167e8b096c0eba35e805cb64d46ad62ae')
    version('1.17.92', sha256='d944a7b999cfe6fee5327a2315c8e5891222c5a88a96e1ca73485978e4990512')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('pkgconfig', type='build')
    depends_on('doxygen',   type='build')
    depends_on('xmlto',     type='build')
    depends_on('libxslt',   type='build')
    depends_on('libxml2')
    depends_on('chrpath')
    depends_on('expat')
    depends_on('libffi')
