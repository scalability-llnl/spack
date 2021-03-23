# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class WaylandProtocols(AutotoolsPackage):
    """wayland-protocols contains Wayland protocols that add functionality not
    available in the Wayland core protocol. Such protocols either add
    completely new functionality, or extend the functionality of some other
    protocol either in Wayland core, or some other protocol i
    n wayland-protocols."""

    homepage = "http://wayland.freedesktop.org/"
    url      = "https://github.com/wayland-project/wayland-protocols/archive/1.20.tar.gz"

    version('1.20',  sha256='b59cf0949aeb1f71f7db46b63b1c5a6705ffde8cb5bd194f843fbd9b41308dda')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('pkgconfig', type='build')
    depends_on('doxygen',   type='build')
    depends_on('xmlto',     type='build')
    depends_on('libxslt',   type='build')
    depends_on('wayland')
