# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import inspect
import os

from spack.directives import depends_on, extends
from spack.package_base import PackageBase, run_after
from spack.util.executable import Executable
from llnl.util.filesystem import filter_file


class PerlPackage(PackageBase):
    """Specialized class for packages that are built using Perl.

    This class provides four phases that can be overridden if required:

        1. :py:meth:`~.PerlPackage.configure`
        2. :py:meth:`~.PerlPackage.build`
        3. :py:meth:`~.PerlPackage.check`
        4. :py:meth:`~.PerlPackage.install`

    The default methods use, in order of preference:
        (1) Makefile.PL,
        (2) Build.PL.

    Some packages may need to override
    :py:meth:`~.PerlPackage.configure_args`,
    which produces a list of arguments for
    :py:meth:`~.PerlPackage.configure`.
    Arguments should not include the installation base directory.
    """
    #: Phases of a Perl package
    phases = ['configure', 'build', 'install']

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'PerlPackage'

    #: Callback names for build-time test
    build_time_test_callbacks = ['check']

    extends('perl')

    depends_on('perl', type=('build', 'run'))

    def configure_args(self):
        """Produces a list containing the arguments that must be passed to
        :py:meth:`~.PerlPackage.configure`. Arguments should not include
        the installation base directory, which is prepended automatically.

        :return: list of arguments for Makefile.PL or Build.PL
        """
        return []

    def configure(self, spec, prefix):
        """Runs Makefile.PL or Build.PL with arguments consisting of
        an appropriate installation base directory followed by the
        list returned by :py:meth:`~.PerlPackage.configure_args`.

        :raise RuntimeError: if neither Makefile.PL or Build.PL exist
        """
        if os.path.isfile('Makefile.PL'):
            self.build_method = 'Makefile.PL'
            self.build_executable = inspect.getmodule(self).make
        elif os.path.isfile('Build.PL'):
            self.build_method = 'Build.PL'
            self.build_executable = Executable(
                os.path.join(self.stage.source_path, 'Build'))
        else:
            raise RuntimeError('Unknown build_method for perl package')

        if self.build_method == 'Makefile.PL':
            options = ['Makefile.PL', 'INSTALL_BASE={0}'.format(prefix)]
        elif self.build_method == 'Build.PL':
            options = ['Build.PL', '--install_base', prefix]
        options += self.configure_args()

        inspect.getmodule(self).perl(*options)

    # It is possible that the shebang in the Build script that is created from
    # Build.PL may be too long causing the build to fail. Patching the shebang
    # does not happen until after install so set '/usr/bin/env perl' here in
    # the Build script.
    @run_after('configure')
    def fix_shebang(self):
        if self.build_method == 'Build.PL':
            pattern = '#!{0}'.format(self.spec['perl'].command.path)
            repl = '#!/usr/bin/env perl'
            filter_file(pattern, repl, 'Build', backup=False)

    def build(self, spec, prefix):
        """Builds a Perl package."""
        self.build_executable()

    # Ensure that tests run after build (if requested):
    run_after('build')(PackageBase._run_default_build_time_test_callbacks)

    def check(self):
        """Runs built-in tests of a Perl package."""
        self.build_executable('test')

    def install(self, spec, prefix):
        """Installs a Perl package."""
        self.build_executable('install')

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
