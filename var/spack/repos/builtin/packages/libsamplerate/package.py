# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsamplerate(AutotoolsPackage):
    """libsamplerate (also known as Secret Rabbit Code) is a library for
    performing sample rate conversion of audio data."""

    homepage = "http://www.mega-nerd.com/libsamplerate/history.html"
    url      = "http://www.mega-nerd.com/libsamplerate/libsamplerate-0.1.9.tar.gz"

    version('0.1.9', sha256='0a7eb168e2f21353fb6d84da152e4512126f7dc48ccb0be80578c565413444c1')
    version('0.1.8', sha256='93b54bdf46d5e6d2354b7034395fe329c222a966790de34520702bb9642f1c06')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
