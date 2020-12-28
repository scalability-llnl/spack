# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Editline(AutotoolsPackage):
    """A readline() replacement for UNIX without termcap (ncurses)"""

    homepage = "http://troglobit.com/editline.html"
    url      = "https://github.com/troglobit/editline/archive/1.16.0.tar.gz"

    version('1.16.0', sha256='33421a1569d025f332a87054bfea28e2c757bdb573f1437bc22c34b798b6383c')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('ncurses')
