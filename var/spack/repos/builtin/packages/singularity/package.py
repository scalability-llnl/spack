# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import llnl.util.tty as tty
import os
import shutil


class Singularity(MakefilePackage):
    '''Singularity is a container technology focused on building portable
       encapsulated environments to support "Mobility of Compute" For older
       versions of Singularity (pre 3.0) you should use singularity-legacy,
       which has a different install base (Autotools).

       Needs post-install chmod/chown steps to enable full functionality.
       See package definition or `spack-build-out.txt` build log for details,
       e.g.

       tail -15 $(spack location -i singularity)/.spack/spack-build-out.txt
    '''

    homepage = "https://sylabs.io/singularity/"
    url      = "https://github.com/hpcng/singularity/releases/download/v3.6.4/singularity-3.6.4.tar.gz"
    git      = "https://github.com/hpcng/singularity.git"

    maintainers = ['alalazo']
    version('master', branch='master')

    version('3.7.2', sha256='36916222e26fb934404f0766e0ff368edac36d7fc31ca571f5f609466609066b')
    version('3.7.1', sha256='82d2c65063560195ec34551931be3c325b95e8e2009e92755fd7daad346e083c')
    version('3.7.0', sha256='fb96aaf5f462a56a4a5bd2951287bcbbefe8cf543e228e4e955428f386a8d478')
    version('3.6.4', sha256='71233a81d6bb4d686d8dc636b3e3e962a372f54001921c89a12b062cefd9e79f')
    version('3.6.3', sha256='b1a985757a9907d8db0f102fc170a25387e715f7ff31957be964bf47914ea2fd')
    version('3.6.2', sha256='dfd7ec7376ca0321c47787388fb3e781034edf99068f66efc36109e516024d9b')
    version('3.6.1', sha256='6cac56106ee7f209150aaee9f8788d03b58796af1b767245d343f0b8a691121c')
    version('3.5.3', sha256='0c76f1e3808bf4c10e92b17150314b2b816be79f8101be448a6e9d7a96c9e486')
    version('3.5.2', sha256='f9c21e289377a4c40ed7a78a0c95e1ff416dec202ed49a6c616dd2c37700eab8')
    version('3.4.1', sha256='638fd7cc5ab2a20e779b8768f73baf21909148339d6c4edf6ff61349c53a70c2')
    version('3.4.0', sha256='eafb27f1ffbed427922ebe2b5b95d1c9c09bfeb897518867444fe230e3e35e41')
    version('3.3.0', sha256='070530a472e7e78492f1f142c8d4b77c64de4626c4973b0589f0d18e1fcf5b4f')
    version('3.2.1', sha256='d4388fb5f7e0083f0c344354c9ad3b5b823e2f3f27980e56efa7785140c9b616')
    version('3.1.1', sha256='7f0df46458d8894ba0c2071b0848895304ae6b1137d3d4630f1600ed8eddf1a4')

    variant('suid', default=True, description='install SUID binary')
    variant('network', default=True, description='install network plugins')

    depends_on('pkgconfig', type='build')
    depends_on('go')
    depends_on('uuid')
    depends_on('libgpg-error')
    depends_on('libseccomp')
    depends_on('squashfs', type='run')
    depends_on('git', when='@develop')  # mconfig uses it for version info
    depends_on('shadow', type='run', when='@3.3:')
    depends_on('cryptsetup', type=('build', 'run'), when='@3.4:')

    patch('singularity_v3.4.0_remove_root_check.patch', level=0, when='@3.4.0:3.4.1')

    # Go has novel ideas about how projects should be organized.
    # We'll point GOPATH at the stage dir, and move the unpacked src
    # tree into the proper subdir in our overridden do_stage below.
    @property
    def gopath(self):
        return self.stage.path

    @property
    def sylabs_gopath_dir(self):
        return join_path(self.gopath, 'src/github.com/sylabs/')

    @property
    def singularity_gopath_dir(self):
        return join_path(self.sylabs_gopath_dir, 'singularity')

    # Unpack the tarball as usual, then move the src dir into
    # its home within GOPATH.
    def do_stage(self, mirror_only=False):
        super(Singularity, self).do_stage(mirror_only)
        if not os.path.exists(self.singularity_gopath_dir):
            # Move the expanded source to its destination
            tty.debug("Moving {0} to {1}".format(
                self.stage.source_path, self.singularity_gopath_dir))
            shutil.move(self.stage.source_path, self.singularity_gopath_dir)

            # The build process still needs access to the source path,
            # so create a symlink.
            force_symlink(self.singularity_gopath_dir, self.stage.source_path)

    # MakefilePackage's stages use this via working_dir()
    @property
    def build_directory(self):
        return self.singularity_gopath_dir

    # Hijack the edit stage to run mconfig.
    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            confstring = './mconfig --prefix=%s' % prefix
            if '~suid' in spec:
                confstring += ' --without-suid'
            if '~network' in spec:
                confstring += ' --without-network'
            configure = Executable(confstring)
            configure()

    # Set these for use by MakefilePackage's default build/install methods.
    build_targets = ['-C', 'builddir', 'parallel=False']
    install_targets = ['install', '-C', 'builddir', 'parallel=False']

    def setup_build_environment(self, env):
        # Point GOPATH at the top of the staging dir for the build step.
        env.prepend_path('GOPATH', self.gopath)

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
        if self.spec.satisfies('+suid'):
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
        if self.spec.satisfies('+suid'):
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
