# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import contextlib
import json
import os
import sys
try:
    import sysconfig  # novm
except ImportError:
    # Not supported on Python 2.6
    pass

import archspec.cpu

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.architecture
import spack.config
import spack.main
import spack.paths
import spack.repo
import spack.spec
import spack.store
import spack.user_environment as uenv
import spack.util.executable
from spack.util.environment import EnvironmentModifications


def spec_for_current_python():
    """For bootstrapping purposes we are just interested in the Python
    minor version (all patches are ABI compatible with the same minor)
    and on whether ucs4 support has been enabled for Python 2.7

    See:
      https://www.python.org/dev/peps/pep-0513/
      https://stackoverflow.com/a/35801395/771663
    """
    version_str = '.'.join(str(x) for x in sys.version_info[:2])
    variant_str = ''
    if sys.version_info[0] == 2 and sys.version_info[1] == 7:
        unicode_size = sysconfig.get_config_var('Py_UNICODE_SIZE')
        variant_str = '+ucs4' if unicode_size == 4 else '~ucs4'

    spec_fmt = 'python@{0} {1}'
    return spec_fmt.format(version_str, variant_str)


@contextlib.contextmanager
def spack_python_interpreter():
    """Override the current configuration to set the interpreter under
    which Spack is currently running as the only Python external spec
    available.
    """
    python_prefix = os.path.dirname(os.path.dirname(sys.executable))
    external_python = spec_for_current_python()

    entry = {
        'buildable': False,
        'externals': [
            {'prefix': python_prefix, 'spec': str(external_python)}
        ]
    }

    with spack.config.override('packages:python::', entry):
        yield


def ensure_module_importable_or_raise(module, abstract_spec=None, install_fn=None):
    """Make the requested module available for import, or raise.

    This function tries to import a Python module in the current interpreter
    using, in the following order, a few different strategies:

        1. Use the default Python import mechanism
        2. Search installed specs in the DB that might provide the module
        3. Install new specs that might provide the module (optional)

    If none of the methods succeed, an exception is raised. The function exits
    on first success.

    Args:
        module (str): module to be imported in the current interpreter
        abstract_spec (str): abstract spec that might provide the module. If not
            given it defaults to "module"
        install_fn (callable): optional callable to try install software that might
            provide the required module. The callable takes a module and an abstract
            spec as arguments

    Raises:
        ImportError: if the module couldn't be imported
    """
    # If we already can import it, that's great
    tty.debug("[BOOTSTRAP MODULE {0}] Try importing from Python".format(module))
    if _python_import(module):
        return

    abstract_spec = abstract_spec or module

    # We have to run as part of this python interpreter
    abstract_spec += ' ^' + spec_for_current_python()

    # Check if any of the already installed specs provide the import
    msg = "[BOOTSTRAP MODULE {0}] Try installed specs with query '{1}'"
    tty.debug(msg.format(module, abstract_spec))
    if _import_from_store(module, abstract_spec):
        return

    # Install software and try to import from that
    install_fn = install_fn or (lambda m, s: False)
    if install_fn(module, abstract_spec):
        return

    # We couldn't import in any way, so raise an import error
    msg = 'cannot import module "{0}"'.format(module)
    if abstract_spec:
        msg += ' from spec "{0}'.format(abstract_spec)
    raise ImportError(msg)


def _python_import(module):
    try:
        __import__(module)
    except ImportError:
        return False
    return True


def _import_from_store(module, spec):
    installed_specs = spack.store.db.query(spec, installed=True)

    for ispec in installed_specs:
        module_path = os.path.join(
            ispec.prefix, ispec['python'].package.site_packages_dir
        )
        module_path_64 = module_path.replace('/lib/', '/lib64/')
        sys.path.append(module_path)
        sys.path.append(module_path_64)

        if _python_import(module):
            return True

        tty.warn("Spec %s did not provide module %s" % (ispec, module))
        sys.path = sys.path[:-2]

    return False


def _try_install_from_sources(module, spec):
    assert spec.concrete, '"{0}" is not a concrete spec'.format(spec)

    # Install the spec that should make the module importable
    spec.package.do_install()

    module_path = os.path.join(
        spec.prefix, spec['python'].package.site_packages_dir
    )
    module_path_64 = module_path.replace('/lib/', '/lib64/')

    sys.path.append(module_path)
    sys.path.append(module_path_64)
    if _python_import(module):
        return True

    sys.path = sys.path[:-2]
    return False


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
    tty.debug('[BOOTSTRAP CONFIG SCOPE] name=_builtin')
    config_scopes = [
        spack.config.InternalConfigScope('_builtin', spack.config.config_defaults)
    ]
    for name, path in spack.config.configuration_paths:
        platform = spack.architecture.platform().name
        platform_scope = spack.config.ConfigScope(
            '/'.join([name, platform]), os.path.join(path, platform)
        )
        generic_scope = spack.config.ConfigScope(name, path)
        config_scopes.extend([generic_scope, platform_scope])
        msg = '[BOOTSTRAP CONFIG SCOPE] name={0}, path={1}'
        tty.debug(msg.format(generic_scope.name, generic_scope.path))
        tty.debug(msg.format(platform_scope.name, platform_scope.path))
    return config_scopes


def _install_clingo_and_try_import(module, abstract_spec_str):
    # This import is local since it is needed only on Cray
    import spack.platforms.linux

    # Read information on verified clingo binaries
    clingo_json_path = os.path.join(
        spack.paths.share_path, 'bootstrap', 'clingo.json'
    )
    with open(clingo_json_path) as f:
        data = json.load(f)

    # Try to install from an unsigned binary cache
    bincache_platform = spack.architecture.real_platform()
    abstract_spec = spack.spec.Spec(abstract_spec_str)

    # On Cray we want to use Linux binaries if available from mirrors
    if str(bincache_platform) == 'cray':
        bincache_platform = spack.platforms.linux.Linux()
        with spack.architecture.use_platform(bincache_platform):
            abstract_spec = spack.spec.Spec(abstract_spec_str)
            if _import_from_store(module, abstract_spec):
                return True

    buildcache = spack.main.SpackCommand('buildcache')
    for item in data['verified']:
        candidate_spec = item['spec']
        python_spec = item['python']
        # Skip specs which are not compatible
        if not abstract_spec.satisfies(candidate_spec):
            continue

        if python_spec not in abstract_spec:
            continue

        msg = "[BOOTSTRAP MODULE {0}] Try installing '{1}' from binary cache"
        tty.debug(msg.format(module, abstract_spec))
        spec_str = '/' + item['hash']
        with spack.architecture.use_platform(bincache_platform):
            with spack.config.override(
                    'compilers', [{'compiler': item['compiler']}]
            ):
                # FIXME: need to check sha256
                install_args = ['install', '-a', '-u', '-o', '-f', spec_str]
                buildcache(*install_args, fail_on_error=False)
                if _import_from_store(module, abstract_spec):
                    return True

        # TODO: uninstall stuff?

    # Try to build and install from sources
    with spack_python_interpreter():
        # Add hint to use frontend operating system on Cray
        if str(spack.architecture.platform()) == 'cray':
            abstract_spec_str = clingo_root_spec()
            abstract_spec_str += ' os=fe ^' + spec_for_current_python()

        concrete_spec = spack.spec.Spec(abstract_spec_str)
        # TODO: substitute this call when the old concretizer is deprecated
        concrete_spec._old_concretize()

    msg = "[BOOTSTRAP MODULE {0}] Try installing '{1}' from sources"
    tty.debug(msg.format(module, abstract_spec_str))
    if _try_install_from_sources(module, concrete_spec):
        return True

    return False


@contextlib.contextmanager
def ensure_bootstrap_configuration():
    with spack.architecture.use_platform(spack.architecture.real_platform()):
        with spack.repo.use_repositories(spack.paths.packages_path):
            with spack.store.use_store(spack.paths.user_bootstrap_store):
                # Default configuration scopes excluding command line
                # and builtin but accounting for platform specific scopes
                config_scopes = _bootstrap_config_scopes()
                with spack.config.use_configuration(*config_scopes):
                    with spack_python_interpreter():
                        yield


def clingo_root_spec():
    # Construct the root spec that will be used to bootstrap clingo
    spec_str = 'clingo-bootstrap@spack+python'

    # Add a proper compiler hint to the root spec. We use GCC for
    # everything but MacOS.
    if str(spack.architecture.platform()) == 'darwin':
        spec_str += ' %apple-clang'
    else:
        spec_str += ' %gcc'

    # Add the generic target
    generic_target = archspec.cpu.host().family
    spec_str += ' target={0}'.format(str(generic_target))

    tty.debug('[BOOTSTRAP ROOT SPEC] clingo: {0}'.format(spec_str))

    return spec_str


def ensure_clingo_importable_or_raise():
    """Ensure that the clingo module is available for import."""
    ensure_module_importable_or_raise(
        module='clingo',
        abstract_spec=clingo_root_spec(),
        install_fn=_install_clingo_and_try_import
    )
