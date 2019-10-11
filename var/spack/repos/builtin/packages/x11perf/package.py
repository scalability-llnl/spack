# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class X11perf(AutotoolsPackage):
    """Simple X server performance benchmarker."""

    homepage = "http://cgit.freedesktop.org/xorg/app/x11perf"
    url      = "https://www.x.org/archive/individual/app/x11perf-1.6.0.tar.gz"

    version('1.6.0', sha256='d33051c4e93100ab60609aee14ff889bb2460f28945063d793e21eda19381abb')

    depends_on('libx11')
    depends_on('libxmu')
    depends_on('libxrender')
    depends_on('libxft')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
