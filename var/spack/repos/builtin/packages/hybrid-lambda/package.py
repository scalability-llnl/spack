# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class HybridLambda(AutotoolsPackage):
    """Hybrid-Lambda is a software package that can simulate gene trees
       within a rooted species network or a rooted species tree under the
       coalescent process.

       The main feature of this program is that users can
       choose to use the standard Kingman coalescent process, which produces
       bifurcating genealogies, or two other Lambda coalescent processes,
       which produce multifurcating genealogies. The other feature is that
       hybrid sim uses extended Newick formatted strings to make it easier to
       represent hybridization events between species."""

    homepage = "https://github.com/hybridLambda/hybrid-Lambda"
    git      = "https://github.com/hybridLambda/hybrid-Lambda.git"

    version('develop', submodules=True)

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('boost')
    depends_on('cppunit', type='test')

    build_directory = 'src'

    @run_after('configure')
    def change_install_option_in_makefile(self):
        with working_dir('src'):
            filter_file(r'INSTALL = /bin/install -c',
                        'INSTALL = /bin/install -C', 'Makefile')
