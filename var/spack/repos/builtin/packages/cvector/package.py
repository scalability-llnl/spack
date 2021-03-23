# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cvector(MakefilePackage):
    """CVector -- ANSI C API for Dynamic Arrays"""

    homepage = "http://cvector.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/cvector/cvector/CVector-1.0.3/CVector-1.0.3.tar.gz"

    version('1.0.3', sha256='d3fa92de3cd5ba8697abdbb52080248b2c252a81cf40a8ec639be301518d0ce3')

    depends_on('libtool', type='build')

    def edit(self, spec, prefix):
        mf = FileFilter('Makefile')
        mf.filter(r'^CC.+', "CC = {0}".format(spack_cc))
        mf.filter(r'^INSTALL_PREFIX .+', "INSTALL_PREFIX = {0}".format(prefix))

    def build(self, spec, prefix):
        pass
