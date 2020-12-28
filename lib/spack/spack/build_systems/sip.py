# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import os

from llnl.util.filesystem import working_dir, join_path
from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, extends
from spack.package_base import PackageBase, run_after


class SIPPackage(PackageBase):
    """Specialized class for packages that are built using the
    SIP build system. See https://www.riverbankcomputing.com/software/sip/intro
    for more information.

    This class provides the following phases that can be overridden:

    * configure
    * build
    * install

    The configure phase already adds a set of default flags. To see more
    options, run ``python configure.py --help``.
    """
    # Default phases
    phases = ['configure', 'build', 'install']

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'SIPPackage'

    #: Name of private sip module to install alongside package
    sip_module = 'sip'

    #: Callback names for install-time test
    install_time_test_callbacks = ['test']

    extends('python')

    depends_on('qt')
    depends_on('py-sip')

    import_modules = PythonPackage.import_modules

    def python(self, *args, **kwargs):
        """The python ``Executable``."""
        inspect.getmodule(self).python(*args, **kwargs)

    def configure_file(self):
        """Returns the name of the configure file to use."""
        return 'configure.py'

    def configure(self, spec, prefix):
        """Configure the package."""
        configure = self.configure_file()

        args = self.configure_args()

        python_include_dir = 'python' + str(spec['python'].version.up_to(2))

        args.extend([
            '--verbose',
            '--confirm-license',
            '--qmake', spec['qt'].prefix.bin.qmake,
            '--sip', spec['py-sip'].prefix.bin.sip,
            '--sip-incdir', join_path(spec['py-sip'].prefix.include,
                                      python_include_dir),
            '--bindir', prefix.bin,
            '--destdir', inspect.getmodule(self).site_packages_dir,
        ])

        self.python(configure, *args)

    def configure_args(self):
        """Arguments to pass to configure."""
        return []

    def build(self, spec, prefix):
        """Build the package."""
        args = self.build_args()

        inspect.getmodule(self).make(*args)

    def build_args(self):
        """Arguments to pass to build."""
        return []

    def install(self, spec, prefix):
        """Install the package."""
        args = self.install_args()

        inspect.getmodule(self).make('install', parallel=False, *args)

    def install_args(self):
        """Arguments to pass to install."""
        return []

    # Testing

    test = PythonPackage.test

    run_after('install')(PackageBase._run_default_install_time_test_callbacks)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)

    @run_after('install')
    def extend_path_setup(self):
        # See github issue #14121 and PR #15297
        module = self.spec['py-sip'].variants['module'].value
        if module != 'sip':
            module = module.split('.')[0]
            with working_dir(inspect.getmodule(self).site_packages_dir):
                with open(os.path.join(module, '__init__.py'), 'a') as f:
                    f.write('from pkgutil import extend_path\n')
                    f.write('__path__ = extend_path(__path__, __name__)\n')
