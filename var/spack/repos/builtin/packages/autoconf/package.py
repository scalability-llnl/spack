# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re


class Autoconf(AutotoolsPackage, GNUMirrorPackage):
    """Autoconf -- system configuration part of autotools"""

    homepage = 'https://www.gnu.org/software/autoconf/'
    gnu_mirror_path = 'autoconf/autoconf-2.69.tar.gz'

    version('2.69', sha256='954bd69b391edc12d6a4a51a2dd1476543da5c6bbf05a95b59dc0dd6fd4c2969')
    version('2.62', sha256='83aa747e6443def0ebd1882509c53f5a2133f502ddefa21b3de141c433914bdd')
    version('2.59', sha256='9cd05c73c5fcb1f5ccae53dd6cac36bb8cb9c7b3e97ffae5a7c05c72594c88d8')
    version('2.13', sha256='f0611136bee505811e9ca11ca7ac188ef5323a8e2ef19cffd3edb3cf08fd791e')

    # Note: m4 is not a pure build-time dependency of autoconf. m4 is
    # needed when autoconf runs, not only when autoconf is built.
    depends_on('m4@1.4.6:', type=('build', 'run'))
    depends_on('perl', type=('build', 'run'))

    build_directory = 'spack-build'

    executables = [
        'autoconf', 'autoheader', 'autom4te', 'autoreconf',
        'autoscan', 'autoupdate', 'ifnames'
    ]

    @classmethod
    def determine_spec_details(cls, prefix, exes_in_prefix):
        """Allow ``spack external find autoconf`` to locate
        autoconf installations.

        Parameters:
            prefix (str): the directory containing the executables
            exes_in_prefix (set): the executables that match the regex

        Returns:
            spack.spec.Spec: the spec of this autoconf installation
        """
        # Possible executable names:
        # * autoconf, autoheader, autom4te, autoreconf, autoscan, autoupdate
        # * ifnames
        # Take the first alphabetical executable name and hope for the best
        autoconf = Executable(min(exes_in_prefix))

        output = autoconf('--version', output=str, error=os.devnull)
        match = re.search(r'\(GNU Autoconf\) ([0-9.]+)', output)
        version = ''
        if match:
            version = '@' + match.group(1)

        return Spec(cls.name + version)

    def patch(self):
        # The full perl shebang might be too long; we have to fix this here
        # because autom4te is called during the build
        filter_file('^#! @PERL@ -w',
                    '#! /usr/bin/env perl',
                    'bin/autom4te.in')

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
