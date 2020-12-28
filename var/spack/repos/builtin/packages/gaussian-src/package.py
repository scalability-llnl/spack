# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob
import os

import llnl.util.tty as tty
from spack.package import *


class GaussianSrc(Package):
    """Gaussian is a computer program for computational chemistry.

    This Spack package builds Gaussian from source.

    Needs post-install steps to make it run!
    See package installation log for details."""

    homepage = "http://www.gaussian.com/"
    manual_download = True

    maintainers = ['dev-zero']

    version('16-C.01', sha256='c9eb73a9df5ca8705fcf2d7ce2d5f9aceb05ae663689f54c0a581c9d4d44fffb')

    depends_on('tcsh', type='build')

    # All compilers except for pgi are in conflict:
    for __compiler in spack.compilers.supported_compilers():
        if __compiler != 'pgi':
            conflicts('%{0}'.format(__compiler),
                      msg='Gaussian can only be built with the PGI compiler')

    patch('16-C.01-replace-deprecated-pgf77-with-pgfortran.patch', when='@16-C.01')
    patch('16-C.01-fix-building-c-code-with-pgcc.patch', when='@16-C.01')
    patch('16-C.01-fix-shebangs.patch', when='@16-C.01')

    @property
    def g_name(self):
        return 'g{0}'.format(self.version.up_to(1))

    @property
    def g_root(self):
        return self.prefix.join(self.g_name)

    def url_for_version(self, version):
        return "file://{0}/g{1}.tgz".format(os.getcwd(), version)

    def install(self, spec, prefix):
        # Spacks strips the single dir inside the tarball, but Gaussian
        # needs it -> move them back
        files = os.listdir()
        mkdirp(self.g_name)
        for f in files:
            os.rename(f, join_path(self.g_name, f))

        opts = ['all']
        #  if spec.satisfies('+cuda'):
        #      opts += [spec.variants['cuda_family'].value]

        with working_dir(self.g_name):
            # can only build with tcsh
            tcsh = which('tcsh')
            tcsh('-c', 'source ${0}root/{0}/bsd/{0}.login ;'
                       './bsd/bld{0} {1}'.format(self.g_name, ' '.join(opts)))

            install_tree('./bsd', self.g_root.bsd)
            install_tree('./basis', self.g_root.basis)
            install_tree('./doc', self.g_root.doc)

            for exe in glob.glob('*.exe'):
                install(exe, self.g_root)

            exes = [
                self.g_name,
                'gauopt',
                'gauoptl',
                'ghelp',
                'newzmat',
                'testrt',
                'cubegen',
                'cubman',
                'c8616',
                'ham506',
                'rwfdump',
                'freqchk',
                'freqmem',
                'formchk',
                'demofc',
                'chkchk',
                'solname',
                'gautraj',
                'copychk',
                'pluck',
                'rdmat',
                'wrmat',
                'unfchk',
                'gdrgen',
                'trajgen',
                'mm',
                'grate',
            ]
            for exe in exes:
                install(exe, self.g_root)

    @run_after('install')
    def caveats(self):
        perm_script = 'spack_perms_fix.sh'
        perm_script_path = join_path(self.spec.prefix, perm_script)
        with open(perm_script_path, 'w') as f:
            env = spack.tengine.make_environment(dirs=self.package_dir)
            t = env.get_template(perm_script + '.j2')
            f.write(t.render({'prefix': self.g_root}))
        chmod = which('chmod')
        chmod('0555', perm_script_path)

        tty.warn("""
For a working Gaussian installation, all executable files can only be accessible by
the owner and the group but not the world.

We've installed a script that will make the necessary changes;
read through it and then execute it:

    {0}

If you have to give others access, please customize the group membership of the package
files as documented here:

    https://spack.readthedocs.io/en/latest/build_settings.html#package-permissions"""
                 .format(perm_script_path))

    def setup_build_environment(self, env):
        env.set('{0}root'.format(self.g_name), self.stage.source_path)

    def setup_run_environment(self, env):
        # defaults taken from G16's g16.profile
        env.set('GAUSS_LFLAGS2', '--LindaOptions -s 10000000')
        env.set('_DSM_BARRIER', 'SHM')
        env.set('PGI_TERM', 'trace,abort')

        env.set('{0}root'.format(self.g_name), self.prefix)

        env.prepend_path('GAUSS_EXEDIR', self.g_root)
        env.prepend_path('GAUSS_EXEDIR', self.g_root.bsd)

        env.prepend_path('PATH', self.g_root)
        env.prepend_path('PATH', self.g_root.bsd)

        env.set('GAUSS_LEXEDIR', self.g_root.join('linda-exe'))
        env.set('GAUSS_ARCHDIR', self.g_root.arch)
        env.set('GAUSS_BSDDIR', self.g_root.bsd)
        env.set('G{0}BASIS'.format(self.version.up_to(1)), self.g_root.basis)

        env.prepend_path('LD_LIBRARY_PATH', self.g_root)
        env.prepend_path('LD_LIBRARY_PATH', self.g_root.bsd)
