# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re


class Autoconf(AutotoolsPackage, GNUMirrorPackage):
    """Autoconf -- system configuration part of autotools"""

    homepage = 'https://www.gnu.org/software/autoconf/'
    gnu_mirror_path = 'autoconf/autoconf-2.69.tar.gz'

    version('2.71', sha256='431075ad0bf529ef13cb41e9042c542381103e80015686222b8a9d4abef42a1c')
    version('2.70', sha256='f05f410fda74323ada4bdc4610db37f8dbd556602ba65bc843edb4d4d4a1b2b7')
    version('2.69', sha256='954bd69b391edc12d6a4a51a2dd1476543da5c6bbf05a95b59dc0dd6fd4c2969',
            preferred=True)
    version('2.62', sha256='83aa747e6443def0ebd1882509c53f5a2133f502ddefa21b3de141c433914bdd')
    version('2.59', sha256='9cd05c73c5fcb1f5ccae53dd6cac36bb8cb9c7b3e97ffae5a7c05c72594c88d8')
    version('2.13', sha256='f0611136bee505811e9ca11ca7ac188ef5323a8e2ef19cffd3edb3cf08fd791e')

    # https://savannah.gnu.org/support/?110396
    patch('https://git.savannah.gnu.org/cgit/autoconf.git/patch/?id=05972f49ee632cd98057a3caf82ebfb9574846da',
          sha256='eaa3f69d927a853313a0b06e2117c51adab6377a2278549b05abc5df93643e16',
          when='@2.70')

    # Note: m4 is not a pure build-time dependency of autoconf. m4 is
    # needed when autoconf runs, not only when autoconf is built.
    depends_on('help2man', type='build')
    depends_on('m4@1.4.6:', type=('build', 'run'))
    depends_on('perl', type=('build', 'run'))

    build_directory = 'spack-build'

    tags = ['build-tools']

    executables = [
        '^autoconf$', '^autoheader$', '^autom4te$', '^autoreconf$',
        '^autoscan$', '^autoupdate$', '^ifnames$'
    ]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'\(GNU Autoconf\)\s+(\S+)', output)
        return match.group(1) if match else None

    def patch(self):
        # The full perl shebang might be too long; we have to fix this here
        # because autom4te is called during the build
        patched_file = 'bin/autom4te.in'

        # We save and restore the modification timestamp of the file to prevent
        # regeneration of the respective man page:
        with keep_modification_time(patched_file):
            filter_file('^#! @PERL@ -w',
                        '#! /usr/bin/env perl',
                        patched_file)

    @run_after('install')
    def filter_sbang(self):
        # We have to do this after install because otherwise the install
        # target will try to rebuild the binaries (filter_file updates the
        # timestamps)

        # Revert sbang, so Spack's sbang hook can fix it up
        filter_file('^#! /usr/bin/env perl',
                    '#! {0} -w'.format(self.spec['perl'].command.path),
                    self.prefix.bin.autom4te,
                    backup=False)

    def _make_executable(self, name):
        return Executable(join_path(self.prefix.bin, name))

    def setup_dependent_package(self, module, dependent_spec):
        # Autoconf is very likely to be a build dependency,
        # so we add the tools it provides to the dependent module
        executables = ['autoconf',
                       'autoheader',
                       'autom4te',
                       'autoreconf',
                       'autoscan',
                       'autoupdate',
                       'ifnames']
        for name in executables:
            setattr(module, name, self._make_executable(name))
