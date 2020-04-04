# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import llnl.util.tty as tty


class Singularity(MakefilePackage):
    '''Singularity is a container technology focused on building portable
       encapsulated environments to support "Mobility of Compute" For older
       versions of Singularity (pre 3.0) you should use singularity-legacy,
       which has a different install base (Autotools).

       Needs post-install chmod/chown steps to enable full functionality.
       See package definition or `spack-build-out.txt` build log for details.
    '''

    # RE: go dependencies, modules, and network access at build time:
    # Singularity, from 3.2.0 -> 3.4.2 uses modules, *and* includes a
    # vendored set of dependencies, *and* their build system enforces its
    # use (see L9 of mlocal/frags/go_common_opts.mk) which means that they
    # do not need to download dependencies at build time.
    # It appears that @3.5: they don't commit the vendor dir to their repo
    # but they *DO* include it in the tar.gz files that attach to the releases
    # so things should just work.
    homepage = "https://www.sylabs.io/singularity/"
    url      = "https://github.com/sylabs/singularity/releases/download/v3.1.1/singularity-3.1.1.tar.gz"
    git      = "https://github.com/sylabs/singularity.git"

    maintainers = ['ArangoGutierrez', 'alalazo']
    version('master', branch='master')

    version('3.5.3', sha256='0c76f1e3808bf4c10e92b17150314b2b816be79f8101be448a6e9d7a96c9e486')
    version('3.5.2', sha256='f9c21e289377a4c40ed7a78a0c95e1ff416dec202ed49a6c616dd2c37700eab8')
    version('3.4.1', sha256='638fd7cc5ab2a20e779b8768f73baf21909148339d6c4edf6ff61349c53a70c2')
    version('3.4.0', sha256='eafb27f1ffbed427922ebe2b5b95d1c9c09bfeb897518867444fe230e3e35e41')
    version('3.3.0', sha256='070530a472e7e78492f1f142c8d4b77c64de4626c4973b0589f0d18e1fcf5b4f')
    version('3.2.1', sha256='d4388fb5f7e0083f0c344354c9ad3b5b823e2f3f27980e56efa7785140c9b616')

    depends_on('go@1.11:')
    depends_on('libuuid')
    depends_on('libgpg-error')
    depends_on('squashfs', type='run')
    depends_on('git', when='@develop')  # mconfig uses it for version info
    depends_on('shadow', type='run', when='@3.3:')
    depends_on('cryptsetup', type=('build', 'run'), when='@3.4:')

    patch('singularity_v3.4.0_remove_root_check.patch', level=0, when='@3.4.0:3.4.1')

    # Hijack the edit stage to run mconfig.
    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            configure = Executable('./mconfig --prefix=%s' % prefix)
            configure()

    # Set these for use by MakefilePackage's default build/install methods.
    build_targets = ['-C', 'builddir', 'parallel=False']
    install_targets = ['install', '-C', 'builddir', 'parallel=False']

    # `singularity` has a fixed path where it will look for
    # mksquashfs.  If it lives somewhere else you need to specify the
    # full path in the config file.  This bit uses filter_file to edit
    # the config file, uncommenting and setting the mksquashfs path.
    @run_after('install')
    def fix_mksquashfs_path(self):
        prefix = self.spec.prefix
        squash_path = join_path(self.spec['squashfs'].prefix.bin, 'mksquashfs')
        filter_file(r'^# mksquashfs path =',
                    'mksquashfs path = {0}'.format(squash_path),
                    join_path(prefix.etc, 'singularity', 'singularity.conf'))

    #
    # Assemble a script that fixes the ownership and permissions of several
    # key files, install it, and tty.warn() the user.
    # HEADSUP: https://github.com/spack/spack/pull/10412.
    #
    def perm_script(self):
        return 'spack_perms_fix.sh'

    def perm_script_tmpl(self):
        return "{0}.j2".format(self.perm_script())

    def perm_script_path(self):
        return join_path(self.spec.prefix.bin, self.perm_script())

    def _build_script(self, filename, variable_data):
        with open(filename, 'w') as f:
            env = spack.tengine.make_environment(dirs=self.package_dir)
            t = env.get_template(self.perm_script_tmpl())
            f.write(t.render(variable_data))

    @run_after('install')
    def build_perms_script(self):
        script = self.perm_script_path()
        chown_files = ['libexec/singularity/bin/starter-suid',
                       'etc/singularity/singularity.conf',
                       'etc/singularity/capability.json',
                       'etc/singularity/ecl.toml']
        setuid_files = ['libexec/singularity/bin/starter-suid']
        self._build_script(script, {'prefix': self.spec.prefix,
                                    'chown_files': chown_files,
                                    'setuid_files': setuid_files})
        chmod = which('chmod')
        chmod('555', script)

    # Until tty output works better from build steps, this ends up in
    # the build log.  See https://github.com/spack/spack/pull/10412.
    @run_after('install')
    def caveats(self):
        tty.warn("""
        For full functionality, you'll need to chown and chmod some files
        after installing the package.  This has security implications.
        For details, see:
        https://sylabs.io/guides/2.6/admin-guide/security.html
        https://sylabs.io/guides/3.2/admin-guide/admin_quickstart.html#singularity-security

        We've installed a script that will make the necessary changes;
        read through it and then execute it as root (e.g. via sudo).

        The script is named:

        {0}
        """.format(self.perm_script_path()))
