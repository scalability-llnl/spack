# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libverto(AutotoolsPackage):
    """libverto provides a loop-neutral async api which allows the library
    to expose asynchronous interfaces and offload the choice of the main
    loop to the application."""

    homepage = "https://github.com/latchset/libverto/"
    url      = "https://github.com/latchset/libverto/archive/0.3.1.tar.gz"

    version('0.3.1', sha256='02c7e679577ae7608ed35fe740bec2ef8c58142344cef247f2797ef788d41adc')
    version('0.3.0', sha256='fad201d9d0ac1abf1283d2d78bb3a615f72cfd2a2141673589d93c0cb762b3f1')
    version('0.2.7', sha256='0ef688a8a8690c24714834cc155b067b1c5d3f3194acceb333751deebd50de01')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
