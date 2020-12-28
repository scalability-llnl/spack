# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Alglib(MakefilePackage):
    """ALGLIB is a cross-platform numerical analysis and data processing
    library."""

    homepage = "http://www.alglib.net"
    url      = "http://www.alglib.net/translator/re/alglib-3.11.0.cpp.gpl.tgz"

    version('3.11.0', sha256='34e391594aac89fb354bdaf58c42849489cd1199197398ba98bb69961f42bdb0')

    build_directory = 'src'

    def edit(self, spec, prefix):
        # this package has no build system!
        make_file_src = join_path(os.path.dirname(self.module.__file__),
                                  'Makefile')
        make_file = join_path(self.stage.source_path, 'src', 'Makefile')
        copy(make_file_src, make_file)
        filter_file(r'so', dso_suffix, make_file)

    def install(self, spec, prefix):
        name = 'libalglib.{0}'.format(dso_suffix)
        with working_dir('src'):
            mkdirp(prefix.lib)
            install(name, prefix.lib)
            mkdirp(prefix.include)
            install('*.h', prefix.include)

    @run_after('install')
    def fix_darwin_install(self):
        # The shared libraries are not installed correctly on Darwin:
        if sys.platform == 'darwin':
            fix_darwin_install_name(self.spec.prefix.lib)
