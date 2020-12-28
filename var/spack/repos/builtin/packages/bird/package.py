# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bird(AutotoolsPackage):
    """The BIRD project aims to develop a dynamic IP routing daemon with
    full support of all modern routing protocols, easy to use
    configuration interface and powerful route filtering language,
    primarily targeted on (but not limited to) Linux and other UNIX-like
    systems and distributed under the GNU General Public License."""

    homepage = "http://bird.network.cz/"
    url      = "https://github.com/BIRD/bird/archive/v2.0.2.tar.gz"

    version('2.0.2', sha256='bd42d48fbcc2c0046d544f1183cd98193ff15b792d332ff45f386b0180b09335')
    version('2.0.1', sha256='cd6ea4a39ca97ad16d364bf80f919f0e75eba02dd7fe46be40f55d78d022244a')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('ncurses')
    depends_on('readline')
