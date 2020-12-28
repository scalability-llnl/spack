# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.util.environment import EnvironmentModifications


class Fsl(Package):
    """FSL is a comprehensive library of analysis tools for FMRI, MRI and DTI
       brain imaging data.

       Note: A manual download is required for FSL.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://fsl.fmrib.ox.ac.uk"
    url      = "file://{0}/fsl-5.0.10-sources.tar.gz".format(os.getcwd())
    manual_download = True

    version('5.0.10', '64823172a08aad679833240ba64c8e30')

    depends_on('python', type=('build', 'run'))
    depends_on('expat')
    depends_on('libx11')
    depends_on('glu')
    depends_on('zlib')
    depends_on('libpng')
    depends_on('boost')
    depends_on('sqlite')

    conflicts('%gcc@6:', when='@5.0.10')

    def patch(self):
        # Uncomment lines in source file to allow building from source
        with working_dir(join_path(self.stage.source_path, 'etc', 'fslconf')):
            sourced = FileFilter('fsl.sh')
            sourced.filter('#FSLCONFDIR', 'FSLCONFDIR')
            sourced.filter('#FSLMACHTYPE', 'FSLMACHTYPE')
        # Fix error in build script
        buildscript = FileFilter('build')
        buildscript.filter('mist-clean', 'mist')

    def install(self, spec, prefix):
        build = Executable('./build')
        build()

        install_tree('.', prefix)

    def setup_build_environment(self, env):
        if not self.stage.source_path:
            self.stage.fetch()
            self.stage.expand_archive()

        env.set('FSLDIR', self.stage.source_path)

        # Below is for sourcing purposes during building
        fslsetup = join_path(self.stage.source_path, 'etc', 'fslconf',
                             'fsl.sh')

        if os.path.isfile(fslsetup):
            env.extend(EnvironmentModifications.from_sourcing_file(fslsetup))

    def setup_run_environment(self, env):
        # Here, run-time environment variables are being set manually.
        # Normally these would be added to the modulefile at build-time
        # by sourcing fsl.sh, but incorrect paths were being set, pointing to
        # the staging directory rather than the install directory.
        env.set('FSLDIR', self.prefix)
        env.set('FSLOUTPUTTYPE', 'NIFTI_GZ')
        env.set('FSLMULTIFILEQUIT', 'TRUE')
        env.set('FSLTCLSH', self.prefix.bin.fsltclsh)
        env.set('FSLWISH', self.prefix.bin.fslwish)
        env.set('FSLLOCKDIR', '')
        env.set('FSLMACHINELIST', '')
        env.set('FSLREMOTECALL', '')
        env.set('FSLGECUDAQ', 'cuda.q')

        env.prepend_path('PATH', self.prefix)
