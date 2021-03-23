# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import contextlib
import os
import sys

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.architecture
import spack.config
import spack.paths
import spack.repo
import spack.spec
import spack.store
import spack.user_environment as uenv
import spack.util.executable
from spack.util.environment import EnvironmentModifications


@contextlib.contextmanager
def spack_python_interpreter():
    """Override the current configuration to set the interpreter under
    which Spack is currently running as the only Python external spec
    available.
    """
    python_cls = type(spack.spec.Spec('python').package)
    python_prefix = os.path.dirname(os.path.dirname(sys.executable))
    externals = python_cls.determine_spec_details(
        python_prefix, [os.path.basename(sys.executable)])
    external_python = externals[0]

    entry = {
        'buildable': False,
        'externals': [
            {'prefix': python_prefix, 'spec': str(external_python)}
        ]
    }

    with spack.config.override('packages:python::', entry):
        yield


def make_module_available(module, spec=None, install=False):
    """Ensure module is importable"""
    # If we already can import it, that's great
    try:
        __import__(module)
        return
    except ImportError:
        pass

    # If it's already installed, use it
    # Search by spec
    spec = spack.spec.Spec(spec or module)

    # We have to run as part of this python
    # We can constrain by a shortened version in place of a version range
    # because this spec is only used for querying or as a placeholder to be
    # replaced by an external that already has a concrete version. This syntax
    # is not suffucient when concretizing without an external, as it will
    # concretize to python@X.Y instead of python@X.Y.Z
    spec.constrain('^python@%d.%d' % sys.version_info[:2])
    installed_specs = spack.store.db.query(spec, installed=True)

    for ispec in installed_specs:
        # TODO: make sure run-environment is appropriate
        module_path = os.path.join(ispec.prefix,
                                   ispec['python'].package.site_packages_dir)
        module_path_64 = module_path.replace('/lib/', '/lib64/')
        try:
            sys.path.append(module_path)
            sys.path.append(module_path_64)
            __import__(module)
            return
        except ImportError:
            tty.warn("Spec %s did not provide module %s" % (ispec, module))
            sys.path = sys.path[:-2]

    def _raise_error(module_name, module_spec):
        error_msg = 'cannot import module "{0}"'.format(module_name)
        if module_spec:
            error_msg += ' from spec "{0}'.format(module_spec)
        raise ImportError(error_msg)

    if not install:
        _raise_error(module, spec)

    with spack_python_interpreter():
        # We will install for ourselves, using this python if needed
        # Concretize the spec
        spec.concretize()
    spec.package.do_install()

    module_path = os.path.join(spec.prefix,
                               spec['python'].package.site_packages_dir)
    module_path_64 = module_path.replace('/lib/', '/lib64/')
    try:
        sys.path.append(module_path)
        sys.path.append(module_path_64)
        __import__(module)
        return
    except ImportError:
        sys.path = sys.path[:-2]
        _raise_error(module, spec)


def get_executable(exe, spec=None, install=False):
    """Find an executable named exe, either in PATH or in Spack

    Args:
        exe (str): needed executable name
        spec (Spec or str): spec to search for exe in (default exe)
        install (bool): install spec if not available

    When ``install`` is True, Spack will use the python used to run Spack as an
    external. The ``install`` option should only be used with packages that
    install quickly (when using external python) or are guaranteed by Spack
    organization to be in a binary mirror (clingo)."""
    # Search the system first
    runner = spack.util.executable.which(exe)
    if runner:
        return runner

    # Check whether it's already installed
    spec = spack.spec.Spec(spec or exe)
    installed_specs = spack.store.db.query(spec, installed=True)
    for ispec in installed_specs:
        # filter out directories of the same name as the executable
        exe_path = [exe_p for exe_p in fs.find(ispec.prefix, exe)
                    if fs.is_exe(exe_p)]
        if exe_path:
            ret = spack.util.executable.Executable(exe_path[0])
            envmod = EnvironmentModifications()
            for dep in ispec.traverse(root=True, order='post'):
                envmod.extend(uenv.environment_modifications_for_spec(dep))
            ret.add_default_envmod(envmod)
            return ret
        else:
            tty.warn('Exe %s not found in prefix %s' % (exe, ispec.prefix))

    def _raise_error(executable, exe_spec):
        error_msg = 'cannot find the executable "{0}"'.format(executable)
        if exe_spec:
            error_msg += ' from spec "{0}'.format(exe_spec)
        raise RuntimeError(error_msg)

    # If we're not allowed to install this for ourselves, we can't find it
    if not install:
        _raise_error(exe, spec)

    with spack_python_interpreter():
        # We will install for ourselves, using this python if needed
        # Concretize the spec
        spec.concretize()

    spec.package.do_install()
    # filter out directories of the same name as the executable
    exe_path = [exe_p for exe_p in fs.find(spec.prefix, exe)
                if fs.is_exe(exe_p)]
    if exe_path:
        ret = spack.util.executable.Executable(exe_path[0])
        envmod = EnvironmentModifications()
        for dep in spec.traverse(root=True, order='post'):
            envmod.extend(uenv.environment_modifications_for_spec(dep))
        ret.add_default_envmod(envmod)
        return ret

    _raise_error(exe, spec)


def _bootstrap_config_scopes():
    config_scopes = []
    for name, path in spack.config.configuration_paths:
        platform = spack.architecture.platform().name
        platform_scope = spack.config.ConfigScope(
            '/'.join([name, platform]), os.path.join(path, platform)
        )
        generic_scope = spack.config.ConfigScope(name, path)
        config_scopes.extend([generic_scope, platform_scope])
        msg = '[BOOSTRAP CONFIG SCOPE] name={0}, path={1}'
        tty.debug(msg.format(generic_scope.name, generic_scope.path))
        tty.debug(msg.format(platform_scope.name, platform_scope.path))
    return config_scopes


@contextlib.contextmanager
def ensure_bootstrap_configuration():
    with spack.architecture.use_platform(spack.architecture.real_platform()):
        # Default configuration scopes excluding command line and builtin
        # but accounting for platform specific scopes
        config_scopes = _bootstrap_config_scopes()
        with spack.config.use_configuration(*config_scopes):
            with spack.repo.use_repositories(spack.paths.packages_path):
                with spack.store.use_store(spack.paths.user_bootstrap_store):
                    with spack_python_interpreter():
                        yield
