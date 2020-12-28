# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import inspect

from spack.directives import depends_on
from spack.package_base import PackageBase, run_after


class SConsPackage(PackageBase):
    """Specialized class for packages built using SCons.

    See http://scons.org/documentation.html for more information.

    This class provides the following phases that can be overridden:

    1. :py:meth:`~.SConsPackage.build`
    2. :py:meth:`~.SConsPackage.install`

    Packages that use SCons as a build system are less uniform than packages
    that use other build systems. Developers can add custom subcommands or
    variables that control the build. You will likely need to override
    :py:meth:`~.SConsPackage.build_args` to pass the appropriate variables.
    """
    #: Phases of a SCons package
    phases = ['build', 'install']

    #: To be used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = 'SConsPackage'

    #: Callback names for build-time test
    build_time_test_callbacks = ['build_test']

    depends_on('scons', type='build')

    def build_args(self, spec, prefix):
        """Arguments to pass to build."""
        return []

    def build(self, spec, prefix):
        """Build the package."""
        args = self.build_args(spec, prefix)

        inspect.getmodule(self).scons(*args)

    def install_args(self, spec, prefix):
        """Arguments to pass to install."""
        return []

    def install(self, spec, prefix):
        """Install the package."""
        args = self.install_args(spec, prefix)

        inspect.getmodule(self).scons('install', *args)

    # Testing

    def build_test(self):
        """Run unit tests after build.

        By default, does nothing. Override this if you want to
        add package-specific tests.
        """
        pass

    run_after('build')(PackageBase._run_default_build_time_test_callbacks)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
