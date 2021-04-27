# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libthai(AutotoolsPackage):
    """LibThai is a set of Thai language support routines aimed to ease
    developers' tasks to incorporate Thai language support in their
    applications. It includes important Thai-specific functions e.g.
    word breaking, input and output methods as well as basic character
    and string supports."""

    homepage = "http://linux.thai.net"
    url      = "https://github.com/tlwg/libthai/releases/download/v0.1.28/libthai-0.1.28.tar.xz"

    version('0.1.28', sha256='ffe0a17b4b5aa11b153c15986800eca19f6c93a4025ffa5cf2cab2dcdf1ae911')
    version('0.1.27', sha256='1659fa1b7b1d6562102d7feb8c8c3fd94bb2dc5761ed7dbaae4f300e1c03eff6')

    depends_on('libdatrie')
    depends_on('doxygen@1.8.8:',  type='build')
