# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import copy
import functools
import json
import os
import os.path
import re
import sys
import uuid
from typing import List

import archspec.cpu

import llnl.util.tty as tty
from llnl.util.lang import GroupedExceptionHandler

import spack.binary_distribution
import spack.config
import spack.detection
import spack.environment
import spack.modules
import spack.paths
import spack.platforms
import spack.repo
import spack.spec
import spack.store
import spack.user_environment
import spack.util.environment
import spack.util.executable
import spack.util.path
import spack.util.spack_yaml
import spack.util.url
import spack.version

from .common import _executables_in_store, _python_import, _try_import_from_store
from .config import spack_python_interpreter, spec_for_current_python

#: Name of the file containing metadata about the bootstrapping source
METADATA_YAML_FILENAME = "metadata.yaml"

is_windows = sys.platform == "win32"

#: Map a bootstrapper type to the corresponding class
_bootstrap_methods = {}


def _bootstrapper(type):
    """Decorator to register classes implementing bootstrapping
    methods.

    Args:
        type (str): string identifying the class
    """

    def _register(cls):
        _bootstrap_methods[type] = cls
        return cls

    return _register


class _BootstrapperBase(object):
    """Base class to derive types that can bootstrap software for Spack"""

    config_scope_name = ""

    def __init__(self, conf):
        self.name = conf["name"]
        self.url = conf["info"]["url"]

    @property
    def mirror_url(self):
        # Absolute paths
        if os.path.isabs(self.url):
            return spack.util.url.format(self.url)

        # Check for :// and assume it's an url if we find it
        if "://" in self.url:
            return self.url

        # Otherwise, it's a relative path
        return spack.util.url.format(os.path.join(self.metadata_dir, self.url))

    @property
    def mirror_scope(self):
        return spack.config.InternalConfigScope(
            self.config_scope_name, {"mirrors:": {self.name: self.mirror_url}}
        )


@_bootstrapper(type="buildcache")
class _BuildcacheBootstrapper(_BootstrapperBase):
    """Install the software needed during bootstrapping from a buildcache."""

    def __init__(self, conf):
        super(_BuildcacheBootstrapper, self).__init__(conf)
        self.metadata_dir = spack.util.path.canonicalize_path(conf["metadata"])
        self.last_search = None
        self.config_scope_name = "bootstrap_buildcache-{}".format(uuid.uuid4())

    @staticmethod
    def _spec_and_platform(abstract_spec_str):
        """Return the spec object and platform we need to use when
        querying the buildcache.

        Args:
            abstract_spec_str: abstract spec string we are looking for
        """
        # This import is local since it is needed only on Cray
        import spack.platforms.linux

        # Try to install from an unsigned binary cache
        abstract_spec = spack.spec.Spec(abstract_spec_str)
        # On Cray we want to use Linux binaries if available from mirrors
        bincache_platform = spack.platforms.real_host()
        return abstract_spec, bincache_platform

    def _read_metadata(self, package_name):
        """Return metadata about the given package."""
        json_filename = "{0}.json".format(package_name)
        json_dir = self.metadata_dir
        json_path = os.path.join(json_dir, json_filename)
        with open(json_path) as f:
            data = json.load(f)
        return data

    def _install_by_hash(self, pkg_hash, pkg_sha256, index, bincache_platform):
        index_spec = next(x for x in index if x.dag_hash() == pkg_hash)
        # Reconstruct the compiler that we need to use for bootstrapping
        compiler_entry = {
            "modules": [],
            "operating_system": str(index_spec.os),
            "paths": {
                "cc": "/dev/null",
                "cxx": "/dev/null",
                "f77": "/dev/null",
                "fc": "/dev/null",
            },
            "spec": str(index_spec.compiler),
            "target": str(index_spec.target.family),
        }
        with spack.platforms.use_platform(bincache_platform):
            with spack.config.override("compilers", [{"compiler": compiler_entry}]):
                spec_str = "/" + pkg_hash
                query = spack.binary_distribution.BinaryCacheQuery(all_architectures=True)
                matches = spack.store.find([spec_str], multiple=False, query_fn=query)
                for match in matches:
                    spack.binary_distribution.install_root_node(
                        match, allow_root=True, unsigned=True, force=True, sha256=pkg_sha256
                    )

    def _install_and_test(self, abstract_spec, bincache_platform, bincache_data, test_fn):
        # Ensure we see only the buildcache being used to bootstrap
        with spack.config.override(self.mirror_scope):
            # This index is currently needed to get the compiler used to build some
            # specs that we know by dag hash.
            spack.binary_distribution.binary_index.regenerate_spec_cache()
            index = spack.binary_distribution.update_cache_and_get_specs()

            if not index:
                raise RuntimeError("The binary index is empty")

            for item in bincache_data["verified"]:
                candidate_spec = item["spec"]
                # This will be None for things that don't depend on python
                python_spec = item.get("python", None)
                # Skip specs which are not compatible
                if not abstract_spec.satisfies(candidate_spec):
                    continue

                if python_spec is not None and python_spec not in abstract_spec:
                    continue

                for pkg_name, pkg_hash, pkg_sha256 in item["binaries"]:
                    # TODO: undo installations that didn't complete?
                    self._install_by_hash(pkg_hash, pkg_sha256, index, bincache_platform)

                info = {}
                if test_fn(query_spec=abstract_spec, query_info=info):
                    self.last_search = info
                    return True
        return False

    def try_import(self, module, abstract_spec_str):
        test_fn, info = functools.partial(_try_import_from_store, module), {}
        if test_fn(query_spec=abstract_spec_str, query_info=info):
            return True

        tty.info("Bootstrapping {0} from pre-built binaries".format(module))
        abstract_spec, bincache_platform = self._spec_and_platform(
            abstract_spec_str + " ^" + spec_for_current_python()
        )
        data = self._read_metadata(module)
        return self._install_and_test(abstract_spec, bincache_platform, data, test_fn)

    def try_search_path(self, executables, abstract_spec_str):
        test_fn, info = functools.partial(_executables_in_store, executables), {}
        if test_fn(query_spec=abstract_spec_str, query_info=info):
            self.last_search = info
            return True

        abstract_spec, bincache_platform = self._spec_and_platform(abstract_spec_str)
        tty.info("Bootstrapping {0} from pre-built binaries".format(abstract_spec.name))
        data = self._read_metadata(abstract_spec.name)
        return self._install_and_test(abstract_spec, bincache_platform, data, test_fn)


@_bootstrapper(type="install")
class _SourceBootstrapper(_BootstrapperBase):
    """Install the software needed during bootstrapping from sources."""

    def __init__(self, conf):
        super(_SourceBootstrapper, self).__init__(conf)
        self.metadata_dir = spack.util.path.canonicalize_path(conf["metadata"])
        self.conf = conf
        self.last_search = None
        self.config_scope_name = "bootstrap_source-{}".format(uuid.uuid4())

    def try_import(self, module, abstract_spec_str):
        info = {}
        if _try_import_from_store(module, abstract_spec_str, query_info=info):
            self.last_search = info
            return True

        tty.info("Bootstrapping {0} from sources".format(module))

        # If we compile code from sources detecting a few build tools
        # might reduce compilation time by a fair amount
        _add_externals_if_missing()

        # Try to build and install from sources
        with spack_python_interpreter():
            # Add hint to use frontend operating system on Cray
            concrete_spec = spack.spec.Spec(abstract_spec_str + " ^" + spec_for_current_python())

            if module == "clingo":
                # TODO: remove when the old concretizer is deprecated
                concrete_spec._old_concretize(deprecation_warning=False)
            else:
                concrete_spec.concretize()

        msg = "[BOOTSTRAP MODULE {0}] Try installing '{1}' from sources"
        tty.debug(msg.format(module, abstract_spec_str))

        # Install the spec that should make the module importable
        with spack.config.override(self.mirror_scope):
            concrete_spec.package.do_install(fail_fast=True)

        if _try_import_from_store(module, query_spec=concrete_spec, query_info=info):
            self.last_search = info
            return True
        return False

    def try_search_path(self, executables, abstract_spec_str):
        info = {}
        if _executables_in_store(executables, abstract_spec_str, query_info=info):
            self.last_search = info
            return True

        tty.info("Bootstrapping {0} from sources".format(abstract_spec_str))

        # If we compile code from sources detecting a few build tools
        # might reduce compilation time by a fair amount
        _add_externals_if_missing()

        concrete_spec = spack.spec.Spec(abstract_spec_str)
        if concrete_spec.name == "patchelf":
            concrete_spec._old_concretize(deprecation_warning=False)
        else:
            concrete_spec.concretize()

        msg = "[BOOTSTRAP] Try installing '{0}' from sources"
        tty.debug(msg.format(abstract_spec_str))
        with spack.config.override(self.mirror_scope):
            concrete_spec.package.do_install()
        if _executables_in_store(executables, concrete_spec, query_info=info):
            self.last_search = info
            return True
        return False


def _make_bootstrapper(conf):
    """Return a bootstrap object built according to the
    configuration argument
    """
    btype = conf["type"]
    return _bootstrap_methods[btype](conf)


def source_is_enabled_or_raise(conf):
    """Raise ValueError if the source is not enabled for bootstrapping"""
    trusted, name = spack.config.get("bootstrap:trusted"), conf["name"]
    if not trusted.get(name, False):
        raise ValueError("source is not trusted")


def ensure_module_importable_or_raise(module, abstract_spec=None):
    """Make the requested module available for import, or raise.

    This function tries to import a Python module in the current interpreter
    using, in order, the methods configured in bootstrap.yaml.

    If none of the methods succeed, an exception is raised. The function exits
    on first success.

    Args:
        module (str): module to be imported in the current interpreter
        abstract_spec (str): abstract spec that might provide the module. If not
            given it defaults to "module"

    Raises:
        ImportError: if the module couldn't be imported
    """
    # If we can import it already, that's great
    tty.debug("[BOOTSTRAP MODULE {0}] Try importing from Python".format(module))
    if _python_import(module):
        return

    abstract_spec = abstract_spec or module

    h = GroupedExceptionHandler()

    for current_config in bootstrapping_sources():
        with h.forward(current_config["name"]):
            source_is_enabled_or_raise(current_config)

            b = _make_bootstrapper(current_config)
            if b.try_import(module, abstract_spec):
                return

    assert h, (
        "expected at least one exception to have been raised at this point: "
        "while bootstrapping {0}".format(module)
    )
    msg = 'cannot bootstrap the "{0}" Python module '.format(module)
    if abstract_spec:
        msg += 'from spec "{0}" '.format(abstract_spec)
    if tty.is_debug():
        msg += h.grouped_message(with_tracebacks=True)
    else:
        msg += h.grouped_message(with_tracebacks=False)
        msg += "\nRun `spack --debug ...` for more detailed errors"
    raise ImportError(msg)


def ensure_executables_in_path_or_raise(executables, abstract_spec, cmd_check=None):
    """Ensure that some executables are in path or raise.

    Args:
        executables (list): list of executables to be searched in the PATH,
            in order. The function exits on the first one found.
        abstract_spec (str): abstract spec that provides the executables
        cmd_check (object): callable predicate that takes a
            ``spack.util.executable.Executable`` command and validate it. Should return
            ``True`` if the executable is acceptable, ``False`` otherwise.
            Can be used to, e.g., ensure a suitable version of the command before
            accepting for bootstrapping.

    Raises:
        RuntimeError: if the executables cannot be ensured to be in PATH

    Return:
        Executable object

    """
    cmd = spack.util.executable.which(*executables)
    if cmd:
        if not cmd_check or cmd_check(cmd):
            return cmd

    executables_str = ", ".join(executables)

    h = GroupedExceptionHandler()

    for current_config in bootstrapping_sources():
        with h.forward(current_config["name"]):
            source_is_enabled_or_raise(current_config)

            b = _make_bootstrapper(current_config)
            if b.try_search_path(executables, abstract_spec):
                # Additional environment variables needed
                concrete_spec, cmd = b.last_search["spec"], b.last_search["command"]
                env_mods = spack.util.environment.EnvironmentModifications()
                for dep in concrete_spec.traverse(
                    root=True, order="post", deptype=("link", "run")
                ):
                    env_mods.extend(
                        spack.user_environment.environment_modifications_for_spec(
                            dep, set_package_py_globals=False
                        )
                    )
                cmd.add_default_envmod(env_mods)
                return cmd

    assert h, (
        "expected at least one exception to have been raised at this point: "
        "while bootstrapping {0}".format(executables_str)
    )
    msg = "cannot bootstrap any of the {0} executables ".format(executables_str)
    if abstract_spec:
        msg += 'from spec "{0}" '.format(abstract_spec)
    if tty.is_debug():
        msg += h.grouped_message(with_tracebacks=True)
    else:
        msg += h.grouped_message(with_tracebacks=False)
        msg += "\nRun `spack --debug ...` for more detailed errors"
    raise RuntimeError(msg)


def _add_externals_if_missing():
    search_list = [
        # clingo
        spack.repo.path.get_pkg_class("cmake"),
        spack.repo.path.get_pkg_class("bison"),
        # GnuPG
        spack.repo.path.get_pkg_class("gawk"),
    ]
    if is_windows:
        search_list.append(spack.repo.path.get_pkg_class("winbison"))
    detected_packages = spack.detection.by_executable(search_list)
    spack.detection.update_configuration(detected_packages, scope="bootstrap")


def is_bootstrapping():
    global _REF_COUNT
    return _REF_COUNT > 0


def _root_spec(spec_str):
    """Add a proper compiler and target to a spec used during bootstrapping.

    Args:
        spec_str (str): spec to be bootstrapped. Must be without compiler and target.
    """
    # Add a proper compiler hint to the root spec. We use GCC for
    # everything but MacOS and Windows.
    if str(spack.platforms.host()) == "darwin":
        spec_str += " %apple-clang"
    elif str(spack.platforms.host()) == "windows":
        spec_str += " %msvc"
    else:
        spec_str += " %gcc"

    target = archspec.cpu.host().family
    spec_str += " target={0}".format(target)

    tty.debug("[BOOTSTRAP ROOT SPEC] {0}".format(spec_str))
    return spec_str


def clingo_root_spec():
    """Return the root spec used to bootstrap clingo"""
    return _root_spec("clingo-bootstrap@spack+python")


def ensure_clingo_importable_or_raise():
    """Ensure that the clingo module is available for import."""
    ensure_module_importable_or_raise(module="clingo", abstract_spec=clingo_root_spec())


def gnupg_root_spec():
    """Return the root spec used to bootstrap GnuPG"""
    return _root_spec("gnupg@2.3:")


def ensure_gpg_in_path_or_raise():
    """Ensure gpg or gpg2 are in the PATH or raise."""
    return ensure_executables_in_path_or_raise(
        executables=["gpg2", "gpg"], abstract_spec=gnupg_root_spec()
    )


def patchelf_root_spec():
    """Return the root spec used to bootstrap patchelf"""
    # 0.13.1 is the last version not to require C++17.
    return _root_spec("patchelf@0.13.1:")


def verify_patchelf(patchelf):
    """Older patchelf versions can produce broken binaries, so we
    verify the version here.

    Arguments:

        patchelf (spack.util.executable.Executable): patchelf executable
    """
    out = patchelf("--version", output=str, error=os.devnull, fail_on_error=False).strip()
    if patchelf.returncode != 0:
        return False
    parts = out.split(" ")
    if len(parts) < 2:
        return False
    try:
        version = spack.version.Version(parts[1])
    except ValueError:
        return False
    return version >= spack.version.Version("0.13.1")


def ensure_patchelf_in_path_or_raise():
    """Ensure patchelf is in the PATH or raise."""
    # The old concretizer is not smart and we're doing its job: if the latest patchelf
    # does not concretize because the compiler doesn't support C++17, we try to
    # concretize again with an upperbound @:13.
    try:
        return ensure_executables_in_path_or_raise(
            executables=["patchelf"], abstract_spec=patchelf_root_spec(), cmd_check=verify_patchelf
        )
    except RuntimeError:
        return ensure_executables_in_path_or_raise(
            executables=["patchelf"],
            abstract_spec=_root_spec("patchelf@0.13.1:0.13"),
            cmd_check=verify_patchelf,
        )


###
# Development dependencies
###


def isort_root_spec():
    return _root_spec("py-isort@4.3.5:")


def ensure_isort_in_path_or_raise():
    """Ensure that isort is in the PATH or raise."""
    executable, root_spec = "isort", isort_root_spec()
    return ensure_executables_in_path_or_raise([executable], abstract_spec=root_spec)


def mypy_root_spec():
    return _root_spec("py-mypy@0.900:")


def ensure_mypy_in_path_or_raise():
    """Ensure that mypy is in the PATH or raise."""
    executable, root_spec = "mypy", mypy_root_spec()
    return ensure_executables_in_path_or_raise([executable], abstract_spec=root_spec)


def black_root_spec():
    return _root_spec("py-black")


def ensure_black_in_path_or_raise():
    """Ensure that black is in the PATH or raise."""
    root_spec = black_root_spec()

    def check_black(black_cmd):
        """Ensure sutable black version."""
        try:
            output = black_cmd("--version", output=str)
        except Exception as e:
            tty.debug("Error getting version of %s: %s" % (black_cmd, e))
            return False

        match = re.match("black, ([^ ]+)", output)
        if not match:
            return False

        black_version = spack.version.Version(match.group(1))
        return black_version.satisfies(spack.spec.Spec(root_spec).versions)

    return ensure_executables_in_path_or_raise(["black"], root_spec, check_black)


def flake8_root_spec():
    return _root_spec("py-flake8")


def ensure_flake8_in_path_or_raise():
    """Ensure that flake8 is in the PATH or raise."""
    executable, root_spec = "flake8", flake8_root_spec()
    return ensure_executables_in_path_or_raise([executable], abstract_spec=root_spec)


def all_root_specs(development=False):
    """Return a list of all the root specs that may be used to bootstrap Spack.

    Args:
        development (bool): if True include dev dependencies
    """
    specs = [clingo_root_spec(), gnupg_root_spec(), patchelf_root_spec()]
    if development:
        specs += [isort_root_spec(), mypy_root_spec(), black_root_spec(), flake8_root_spec()]
    return specs


def bootstrapping_sources(scope=None):
    """Return the list of configured sources of software for bootstrapping Spack

    Args:
        scope (str or None): if a valid configuration scope is given, return the
            list only from that scope
    """
    source_configs = spack.config.get("bootstrap:sources", default=None, scope=scope)
    source_configs = source_configs or []
    list_of_sources = []
    for entry in source_configs:
        current = copy.copy(entry)
        metadata_dir = spack.util.path.canonicalize_path(entry["metadata"])
        metadata_yaml = os.path.join(metadata_dir, METADATA_YAML_FILENAME)
        with open(metadata_yaml) as f:
            current.update(spack.util.spack_yaml.load(f))
        list_of_sources.append(current)
    return list_of_sources
