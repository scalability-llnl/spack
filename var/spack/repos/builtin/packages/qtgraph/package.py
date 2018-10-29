# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Qtgraph(QMakePackage):
    """The baseline library used in the CUDA-centric Open|SpeedShop Graphical
       User Interface (GUI) which allows Graphviz DOT formatted data to be
       imported into a Qt application by wrapping the Graphviz libcgraph and
       libgvc within the Qt Graphics View Framework."""

    homepage = "https://github.com/OpenSpeedShop/QtGraph"
    git      = "https://github.com/OpenSpeedShop/QtGraph.git"

    version('develop', branch='master')
    version('1.0.0.0', branch='1.0.0.0')

    # qtgraph depends on these packages
    depends_on('qt@4.8.6:', when='@develop')
    depends_on('qt@5.10.0', when='@1.0.0.0:')

    depends_on("graphviz@2.40.1:", when='@develop')
    depends_on("graphviz@2.40.1", when='@1.0.0.0:')

    def setup_environment(self, spack_env, run_env):
        """Set up the compile and runtime environments for a package."""
        spack_env.set('GRAPHVIZ_ROOT', self.spec['graphviz'].prefix)
        spack_env.set('INSTALL_ROOT', self.prefix)

        # What library suffix should be used based on library existence
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        # The implementor has set up the library and include paths in
        # a non-conventional way.  We reflect that here.
        run_env.prepend_path(
            'LD_LIBRARY_PATH', join_path(
                lib_dir,
                '{0}'.format(self.spec['qt'].version.up_to(3))))

        run_env.prepend_path('CPATH', self.prefix.include.QtGraph)
