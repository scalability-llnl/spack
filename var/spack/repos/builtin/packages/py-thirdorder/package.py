# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyThirdorder(PythonPackage):
    """It helps ShengBTE users create FORCE_CONSTANTS_3RD files efficiently"""

    homepage = "http://www.shengbte.org"
    url      = "http://www.shengbte.org/downloads/thirdorder-v1.1.1-8526f47.tar.bz2"

    version('1.1.1-8526f47', '5e1cc8d6ffa7efdb7325c397ca236863ea8a9c5bed1c558acca68b140f89167e')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('spglib', type=('build', 'run'))

    def patch(self):
        setupfile = FileFilter('setup.py')
        setupfile.filter('LIBRARY_DIRS = .*', 'LIBRARY_DIRS = ["%s"]'
                         % self.spec['spglib'].prefix.lib)
        setupfile.filter('INCLUDE_DIRS = .*', 'INCLUDE_DIRS = ["%s"]'
                         % self.spec['spglib'].prefix.include)

        sourcefile = FileFilter('thirdorder_core.c')
        sourcefile.filter('#include "spglib.*"', '#include "spglib.h"')

    @run_after('install')
    def post_install(self):
        mkdirp(self.prefix.bin)
        install('thirdorder_espresso.py', self.prefix.bin)
        install('thirdorder_vasp.py', self.prefix.bin)
        install('thirdorder_castep.py', self.prefix.bin)
        install('thirdorder_common.py', self.prefix.bin)
