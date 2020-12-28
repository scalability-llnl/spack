# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty
from spack.pkg.builtin.openfoam import add_extra_files
from spack.package import *


class OfPrecice(Package):
    """preCICE adapter for OpenFOAM"""

    homepage = 'https://www.precice.org'
    git      = 'https://github.com/precice/openfoam-adapter.git'

    # Currently develop only
    version('develop', branch='master')

    depends_on('openfoam+source')
    depends_on('precice')
    depends_on('yaml-cpp')

    # General patches
    common = ['change-userdir.sh', 'spack-derived-Allwmake']
    assets = []

    build_script  = './spack-derived-Allwmake'
    build_userdir = 'spack-userdir'  # Build user APPBIN, LIBBIN into here

    phases = ['configure', 'build', 'install']

    #
    # - End of definitions / setup -
    #

    def patch(self):
        """Copy additional files or other patching."""
        add_extra_files(self, self.common, self.assets)
        # Emit openfoam version immediately, if we resolved the wrong version
        # it takes a very long time to rebuild!
        tty.info('Build for ' + self.spec['openfoam'].format(
            '{name}{@version}{%compiler}{compiler_flags}{variants}'
        ))

    def configure(self, spec, prefix):
        """Generate spack-config.sh file."""
        # Local tweaks
        # This is ugly, but otherwise it only looks for src/precice,
        # not the installed include files
        config = join_path(self.stage.source_path, 'spack-config.sh')
        with open(config, 'w') as out:
            out.write(
                """# Local tweaks for building
CPLUS_INCLUDE_PATH="{precice_dir}/include/precice${{CPLUS_INCLUDE_PATH:+:}}$CPLUS_INCLUDE_PATH"  ## noqa: E501
export CPLUS_INCLUDE_PATH
# Local build (for user appbin, libbin)
. ./change-userdir.sh $PWD/{user_dir}
#
"""
                .format(
                    precice_dir=spec['precice'].prefix,
                    user_dir=self.build_userdir))

    def build(self, spec, prefix):
        """Build with Allwmake script, wrapped to source environment first."""
        args = []
        if self.parallel:  # Parallel build? - pass via environment
            os.environ['WM_NCOMPPROCS'] = str(make_jobs)
        builder = Executable(self.build_script)
        builder(*args)

    def install(self, spec, prefix):
        """Install under the prefix directory"""

        for f in ['README.md', 'LICENSE']:
            if os.path.isfile(f):
                install(f, join_path(self.prefix, f))

        install_tree('tutorials', join_path(self.prefix, 'tutorials'))

        # Place directly under 'lib' (no bin)
        install_tree(
            join_path(self.build_userdir, 'lib'),
            join_path(self.prefix, 'lib'))
