# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
import os
import re

import llnl.util.tty as tty
from llnl.util.filesystem import find, join_path, working_dir

import spack.builder
import spack.package
from spack.directives import buildsystem, depends_on, extends
from spack.multimethod import when

sip = spack.builder.BuilderMeta.make_decorator('sip')


class SIPPackage(spack.package.PackageBase):
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
    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'SIPPackage'

    #: Name of private sip module to install alongside package
    sip_module = 'sip'

    #: Callback names for install-time test
    install_time_test_callbacks = ['test']

    buildsystem('sip')
    with when('buildsystem=sip'):
        extends('python')
        depends_on('qt')
        depends_on('py-sip')

    @property
    def import_modules(self):
        """Names of modules that the Python package provides.

        These are used to test whether or not the installation succeeded.
        These names generally come from running:

        .. code-block:: python

           >> import setuptools
           >> setuptools.find_packages()

        in the source tarball directory. If the module names are incorrectly
        detected, this property can be overridden by the package.

        Returns:
            list: list of strings of module names
        """
        modules = []
        root = os.path.join(
            self.prefix,
            self.spec['python'].package.platlib,
        )

        # Some Python libraries are packages: collections of modules
        # distributed in directories containing __init__.py files
        for path in find(root, '__init__.py', recursive=True):
            modules.append(path.replace(root + os.sep, '', 1).replace(
                os.sep + '__init__.py', '').replace('/', '.'))

        # Some Python libraries are modules: individual *.py files
        # found in the site-packages directory
        for path in find(root, '*.py', recursive=False):
            modules.append(path.replace(root + os.sep, '', 1).replace(
                '.py', '').replace('/', '.'))

        modules = [mod for mod in modules if re.match('[a-zA-Z0-9._]+$', mod)]

        tty.debug('Detected the following modules: {0}'.format(modules))

        return modules

    def python(self, *args, **kwargs):
        """The python ``Executable``."""
        inspect.getmodule(self).python(*args, **kwargs)

    def test(self):
        """Attempts to import modules of the installed package."""

        # Make sure we are importing the installed modules,
        # not the ones in the source directory
        for module in self.import_modules:
            self.run_test(inspect.getmodule(self).python.path,
                          ['-c', 'import {0}'.format(module)],
                          purpose='checking import of {0}'.format(module),
                          work_dir='spack-test')


class SIPWrapper(spack.builder.BuildWrapper):
    def configure_file(self):
        """Returns the name of the configure file to use."""
        return 'configure.py'

    def configure(self, spec, prefix):
        """Configure the package."""
        configure = self.configure_file()

        args = self.configure_args()

        args.extend([
            '--verbose',
            '--confirm-license',
            '--qmake', spec['qt'].prefix.bin.qmake,
            '--sip', spec['py-sip'].prefix.bin.sip,
            '--sip-incdir', join_path(spec['py-sip'].prefix,
                                      spec['python'].package.include),
            '--bindir', prefix.bin,
            '--destdir', inspect.getmodule(self).python_platlib,
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

    sip.run_after('install')(
        spack.package.PackageBase._run_default_install_time_test_callbacks
    )

    # Check that self.prefix is there after installation
    sip.run_after('install')(spack.package.PackageBase.sanity_check_prefix)

    @sip.run_after('install')
    def extend_path_setup(self):
        # See github issue #14121 and PR #15297
        module = self.spec['py-sip'].variants['module'].value
        if module != 'sip':
            module = module.split('.')[0]
            with working_dir(inspect.getmodule(self).python_platlib):
                with open(os.path.join(module, '__init__.py'), 'a') as f:
                    f.write('from pkgutil import extend_path\n')
                    f.write('__path__ = extend_path(__path__, __name__)\n')


@spack.builder.builder('sip')
class SIPBuilder(spack.builder.Builder):
    phases = ('configure', 'build', 'install')
    PackageWrapper = SIPWrapper
