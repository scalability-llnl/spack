# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Vmd(Package):
    """VMD provides user-editable materials which can be applied
    to molecular geometry.

    These material properties control the details of how VMD shades
    the molecular geometry, and how transparent or opaque the displayed
    molecular geometry is. With this feature, one can easily create nice
    looking transparent surfaces which allow inner structural details to
    be seen within a large molecular structure. The material controls can
    be particularly helpful when rendering molecular scenes using external
    ray tracers, each of which typically differ slightly.
    """

    homepage = "https://www.ks.uiuc.edu/Research/vmd/"
    version('1.9.3', sha256='145b4d0cc10b56cadeb71e16c54ab8be713e268f11491714cd617422758ec643',
            url='file://{0}/vmd-1.9.3.bin.LINUXAMD64-CUDA8-OptiX4-OSPRay111p1.opengl.tar.gz'.format(os.getcwd()))
    manual_download = True

    phases = ['configure', 'install']

    depends_on('libx11', type=('run', 'link'))
    depends_on('libxi', type=('run', 'link'))
    depends_on('libxinerama', type=('run', 'link'))
    depends_on('gl@3:', type=('run', 'link'))
    depends_on('patchelf', type='build')

    def setup_build_environment(self, env):
        env.set('VMDINSTALLBINDIR', self.prefix.bin)
        env.set('VMDINSTALLLIBRARYDIR', self.prefix.lib64)

    def configure(self, spec, prefix):
        configure = Executable('./configure')
        configure('LINUXAMD64')

    def install(self, spec, prefix):
        with working_dir(join_path(self.stage.source_path, 'src')):
            make('install')

        # make sure the executable finds and uses the Spack-provided
        # libraries, otherwise the executable may or may not run depending
        # on what is installed on the host
        patchelf = which('patchelf')
        rpath = ':'.join(
            self.spec[dep].libs.directories[0]
            for dep in ['libx11', 'libxi', 'libxinerama', 'gl'])
        patchelf('--set-rpath', rpath,
                 join_path(self.prefix, 'lib64', 'vmd_LINUXAMD64'))

    def setup_run_environment(self, env):
        env.set('PLUGINDIR', self.spec.prefix.lib64.plugins)
