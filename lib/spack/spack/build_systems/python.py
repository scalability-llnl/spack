# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
import os
import shutil

from spack.directives import extends
from spack.package import PackageBase, run_after

from llnl.util.filesystem import (working_dir, get_filetype, filter_file,
                                  path_contains_subdirectory, same_path, find)
from llnl.util.lang import match_predicate
import llnl.util.tty as tty


class PythonPackage(PackageBase):
    """Specialized class for packages that are built using Python
    setup.py files

    This class provides the following phases that can be overridden:

    * build
    * build_py
    * build_ext
    * build_clib
    * build_scripts
    * install
    * install_lib
    * install_headers
    * install_scripts
    * install_data

    These are all standard setup.py commands and can be found by running:

    .. code-block:: console

       $ python setup.py --help-commands

    By default, only the 'build' and 'install' phases are run, but if you
    need to run more phases, simply modify your ``phases`` list like so:

    .. code-block:: python

       phases = ['build_ext', 'install', 'bdist']

    Each phase provides a function <phase> that runs:

    .. code-block:: console

       $ python -s setup.py --no-user-cfg <phase>

    Each phase also has a <phase_args> function that can pass arguments to
    this call. All of these functions are empty except for the ``install_args``
    function, which passes ``--prefix=/path/to/installation/directory``.

    If you need to run a phase which is not a standard setup.py command,
    you'll need to define a function for it like so:

    .. code-block:: python

       def configure(self, spec, prefix):
           self.setup_py('configure')
    """
    #: Package name, version, and extension on PyPI
    pypi = None

    maintainers = ['adamjstewart']

    # Default phases
    phases = ['build', 'install']

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'PythonPackage'

    #: Callback names for install-time test
    install_time_test_callbacks = ['test']

    extends('python')

    py_namespace = None

    @property
    def homepage(self):
        if self.pypi:
            name = self.pypi.split('/')[0]
            return 'https://pypi.org/project/' + name + '/'

    @property
    def url(self):
        if self.pypi:
            return (
                'https://files.pythonhosted.org/packages/source/'
                + self.pypi[0] + '/' + self.pypi
            )

    @property
    def list_url(self):
        if self.pypi:
            name = self.pypi.split('/')[0]
            return 'https://pypi.org/simple/' + name + '/'

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

        # Python libraries may be installed in lib or lib64
        # See issues #18520 and #17126
        for lib in ['lib', 'lib64']:
            root = os.path.join(self.prefix, lib, 'python{0}'.format(
                self.spec['python'].version.up_to(2)), 'site-packages')
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

        tty.debug('Detected the following modules: {0}'.format(modules))
        return modules

    def setup_file(self):
        """Returns the name of the setup file to use."""
        return 'setup.py'

    @property
    def build_directory(self):
        """The directory containing the ``setup.py`` file."""
        return self.stage.source_path

    def python(self, *args, **kwargs):
        inspect.getmodule(self).python(*args, **kwargs)

    def setup_py(self, *args, **kwargs):
        setup = self.setup_file()

        with working_dir(self.build_directory):
            self.python('-s', setup, '--no-user-cfg', *args, **kwargs)

    # The following phases and their descriptions come from:
    #   $ python setup.py --help-commands

    # Standard commands

    def build(self, spec, prefix):
        """Build everything needed to install."""
        args = self.build_args(spec, prefix)

        self.setup_py('build', *args)

    def build_args(self, spec, prefix):
        """Arguments to pass to build."""
        return []

    def build_py(self, spec, prefix):
        '''"Build" pure Python modules (copy to build directory).'''
        args = self.build_py_args(spec, prefix)

        self.setup_py('build_py', *args)

    def build_py_args(self, spec, prefix):
        """Arguments to pass to build_py."""
        return []

    def build_ext(self, spec, prefix):
        """Build C/C++ extensions (compile/link to build directory)."""
        args = self.build_ext_args(spec, prefix)

        self.setup_py('build_ext', *args)

    def build_ext_args(self, spec, prefix):
        """Arguments to pass to build_ext."""
        return []

    def build_clib(self, spec, prefix):
        """Build C/C++ libraries used by Python extensions."""
        args = self.build_clib_args(spec, prefix)

        self.setup_py('build_clib', *args)

    def build_clib_args(self, spec, prefix):
        """Arguments to pass to build_clib."""
        return []

    def build_scripts(self, spec, prefix):
        '''"Build" scripts (copy and fixup #! line).'''
        args = self.build_scripts_args(spec, prefix)

        self.setup_py('build_scripts', *args)

    def build_scripts_args(self, spec, prefix):
        """Arguments to pass to build_scripts."""
        return []

    def install(self, spec, prefix):
        """Install everything from build directory."""
        args = self.install_args(spec, prefix)

        self.setup_py('install', *args)

    def install_args(self, spec, prefix):
        """Arguments to pass to install."""
        args = ['--prefix={0}'.format(prefix)]

        # This option causes python packages (including setuptools) NOT
        # to create eggs or easy-install.pth files.  Instead, they
        # install naturally into $prefix/pythonX.Y/site-packages.
        #
        # Eggs add an extra level of indirection to sys.path, slowing
        # down large HPC runs.  They are also deprecated in favor of
        # wheels, which use a normal layout when installed.
        #
        # Spack manages the package directory on its own by symlinking
        # extensions into the site-packages directory, so we don't really
        # need the .pth files or egg directories, anyway.
        #
        # We need to make sure this is only for build dependencies. A package
        # such as py-basemap will not build properly with this flag since
        # it does not use setuptools to build and those does not recognize
        # the --single-version-externally-managed flag
        if ('py-setuptools' == spec.name or          # this is setuptools, or
            'py-setuptools' in spec._dependencies and  # it's an immediate dep
            'build' in spec._dependencies['py-setuptools'].deptypes):
            args += ['--single-version-externally-managed']

        # Get all relative paths since we set the root to `prefix`
        # We query the python with which these will be used for the lib and inc
        # directories. This ensures we use `lib`/`lib64` as expected by python.
        python = spec['python'].package.command
        command_start = 'print(distutils.sysconfig.'
        commands = ';'.join([
            'import distutils.sysconfig',
            command_start + 'get_python_lib(plat_specific=False, prefix=""))',
            command_start + 'get_python_lib(plat_specific=True, prefix=""))',
            command_start + 'get_python_inc(plat_specific=True, prefix=""))'])
        pure_site_packages_dir, plat_site_packages_dir, inc_dir = python(
            '-c', commands, output=str, error=str).strip().split('\n')

        args += ['--root=%s' % prefix,
                 '--install-purelib=%s' % pure_site_packages_dir,
                 '--install-platlib=%s' % plat_site_packages_dir,
                 '--install-scripts=bin',
                 '--install-data=',
                 '--install-headers=%s' % inc_dir
                 ]

        return args

    def install_lib(self, spec, prefix):
        """Install all Python modules (extensions and pure Python)."""
        args = self.install_lib_args(spec, prefix)

        self.setup_py('install_lib', *args)

    def install_lib_args(self, spec, prefix):
        """Arguments to pass to install_lib."""
        return []

    def install_headers(self, spec, prefix):
        """Install C/C++ header files."""
        args = self.install_headers_args(spec, prefix)

        self.setup_py('install_headers', *args)

    def install_headers_args(self, spec, prefix):
        """Arguments to pass to install_headers."""
        return []

    def install_scripts(self, spec, prefix):
        """Install scripts (Python or otherwise)."""
        args = self.install_scripts_args(spec, prefix)

        self.setup_py('install_scripts', *args)

    def install_scripts_args(self, spec, prefix):
        """Arguments to pass to install_scripts."""
        return []

    def install_data(self, spec, prefix):
        """Install data files."""
        args = self.install_data_args(spec, prefix)

        self.setup_py('install_data', *args)

    def install_data_args(self, spec, prefix):
        """Arguments to pass to install_data."""
        return []

    # Testing

    def test(self):
        """Attempts to import modules of the installed package."""

        # Make sure we are importing the installed modules,
        # not the ones in the source directory
        for module in self.import_modules:
            self.run_test(inspect.getmodule(self).python.path,
                          ['-c', 'import {0}'.format(module)],
                          purpose='checking import of {0}'.format(module),
                          work_dir='spack-test')

    run_after('install')(PackageBase._run_default_install_time_test_callbacks)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)

    def view_file_conflicts(self, view, merge_map):
        """Report all file conflicts, excepting special cases for python.
           Specifically, this does not report errors for duplicate
           __init__.py files for packages in the same namespace.
        """
        conflicts = list(dst for src, dst in merge_map.items()
                         if os.path.exists(dst))

        if conflicts and self.py_namespace:
            ext_map = view.extensions_layout.extension_map(self.extendee_spec)
            namespaces = set(
                x.package.py_namespace for x in ext_map.values())
            namespace_re = (
                r'site-packages/{0}/__init__.py'.format(self.py_namespace))
            find_namespace = match_predicate(namespace_re)
            if self.py_namespace in namespaces:
                conflicts = list(
                    x for x in conflicts if not find_namespace(x))

        return conflicts

    def add_files_to_view(self, view, merge_map):
        bin_dir = self.spec.prefix.bin
        python_prefix = self.extendee_spec.prefix
        python_is_external = self.extendee_spec.external
        global_view = same_path(python_prefix, view.get_projection_for_spec(
            self.spec
        ))
        for src, dst in merge_map.items():
            if os.path.exists(dst):
                continue
            elif global_view or not path_contains_subdirectory(src, bin_dir):
                view.link(src, dst)
            elif not os.path.islink(src):
                shutil.copy2(src, dst)
                is_script = 'script' in get_filetype(src)
                if is_script and not python_is_external:
                    filter_file(
                        python_prefix, os.path.abspath(
                            view.get_projection_for_spec(self.spec)), dst
                    )
            else:
                orig_link_target = os.path.realpath(src)
                new_link_target = os.path.abspath(merge_map[orig_link_target])
                view.link(new_link_target, dst)

    def remove_files_from_view(self, view, merge_map):
        ignore_namespace = False
        if self.py_namespace:
            ext_map = view.extensions_layout.extension_map(self.extendee_spec)
            remaining_namespaces = set(
                spec.package.py_namespace for name, spec in ext_map.items()
                if name != self.name)
            if self.py_namespace in remaining_namespaces:
                namespace_init = match_predicate(
                    r'site-packages/{0}/__init__.py'.format(self.py_namespace))
                ignore_namespace = True

        bin_dir = self.spec.prefix.bin
        global_view = (
            self.extendee_spec.prefix == view.get_projection_for_spec(
                self.spec
            )
        )
        for src, dst in merge_map.items():
            if ignore_namespace and namespace_init(dst):
                continue

            if global_view or not path_contains_subdirectory(src, bin_dir):
                view.remove_file(src, dst)
            else:
                os.remove(dst)
