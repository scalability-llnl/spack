# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import contextlib
import os
import sys

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.spec
import spack.store
import spack.user_environment as uenv
import spack.util.executable
from spack.util.environment import EnvironmentModifications


@contextlib.contextmanager
def system_python_context():
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

    if not install:
        raise Exception  # TODO specify

    with system_python_context():
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
        raise Exception  # TODO: specify


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
    # Easy, we found it externally
    # TODO: Add to externals/database?
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

    # If we're not allowed to install this for ourselves, we can't find it
    if not install:
        raise Exception  # TODO specify

    with system_python_context():
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

    raise Exception  # TODO specify
