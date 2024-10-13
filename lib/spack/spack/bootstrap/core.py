# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Bootstrap Spack core dependencies from binaries.

This module contains logic to bootstrap software required by Spack from binaries served in the
bootstrapping mirrors. The logic is quite different from an installation done from a Spack user,
because of the following reasons:

  1. The binaries are all compiled on the same OS for a given platform (e.g. they are compiled on
     ``centos7`` on ``linux``), but they will be installed and used on the host OS. They are also
     targeted at the most generic architecture possible. That makes the binaries difficult to reuse
     with other specs in an environment without ad-hoc logic.
  2. Bootstrapping has a fallback procedure where we try to install software by default from the
     most recent binaries, and proceed to older versions of the mirror, until we try building from
     sources as a last resort. This allows us not to be blocked on architectures where we don't
     have binaries readily available, but is also not compatible with the working of environments
     (they don't have fallback procedures).
  3. Among the binaries we have clingo, so we can't concretize that with clingo :-)
  4. clingo, GnuPG and patchelf binaries need to be verified by sha256 sum (all the other binaries
     we might add on top of that in principle can be verified with GPG signatures).
"""

import copy
import functools
import json
import os
import os.path
import sys
import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple

from llnl.util import tty
from llnl.util.lang import GroupedExceptionHandler

import spack.binary_distribution
import spack.config
import spack.detection
import spack.platforms
import spack.spec
import spack.store
import spack.user_environment
import spack.util.executable
import spack.util.path
import spack.util.spack_yaml
import spack.util.url
import spack.version
from spack.installer import PackageInstaller

from ._common import _executables_in_store, _python_import, _root_spec, _try_import_from_store
from .clingo import ClingoBootstrapConcretizer
from .config import spack_python_interpreter, spec_for_current_python

#: Name of the file containing metadata about the bootstrapping source
METADATA_YAML_FILENAME = "metadata.yaml"

#: Whether the current platform is Windows
IS_WINDOWS = sys.platform == "win32"

#: Map a bootstrapper type to the corresponding class
_bootstrap_methods = {}


ConfigDictionary = Dict[str, Any]


def bootstrapper(bootstrapper_type: str):
    """Decorator to register classes implementing bootstrapping
    methods.

    Args:
        bootstrapper_type: string identifying the class
    """

    def _register(cls):
        _bootstrap_methods[bootstrapper_type] = cls
        return cls

    return _register


class Bootstrapper:
    """Interface for "core" software bootstrappers"""

    config_scope_name = ""

    def __init__(self, conf: ConfigDictionary) -> None:
        self.conf = conf
        self.name = conf["name"]
        self.metadata_dir = spack.util.path.canonicalize_path(conf["metadata"])

        # Promote (relative) paths to file urls
        url = conf["info"]["url"]
        if spack.util.url.is_path_instead_of_url(url):
            if not os.path.isabs(url):
                url = os.path.join(self.metadata_dir, url)
            url = spack.util.url.path_to_file_url(url)
        self.url = url

    @property
    def mirror_scope(self) -> spack.config.InternalConfigScope:
        """Mirror scope to be pushed onto the bootstrapping configuration when using
        this bootstrapper.
        """
        return spack.config.InternalConfigScope(
            self.config_scope_name, {"mirrors:": {self.name: self.url}}
        )

    def try_import(self, module: str, abstract_spec_str: str) -> bool:
        """Try to import a Python module from a spec satisfying the abstract spec
        passed as argument.

        Args:
            module: Python module name to try importing
            abstract_spec_str: abstract spec that can provide the Python module

        Return:
            True if the Python module could be imported, False otherwise
        """
        return False

    def try_search_path(self, executables: Tuple[str], abstract_spec_str: str) -> bool:
        """Try to search some executables in the prefix of specs satisfying the abstract
        spec passed as argument.

        Args:
            executables: executables to be found
            abstract_spec_str: abstract spec that can provide the Python module

        Return:
            True if the executables are found, False otherwise
        """
        return False


@bootstrapper(bootstrapper_type="buildcache")
class BuildcacheBootstrapper(Bootstrapper):
    """Install the software needed during bootstrapping from a buildcache."""

    def __init__(self, conf) -> None:
        super().__init__(conf)
        self.last_search: Optional[ConfigDictionary] = None
        self.config_scope_name = f"bootstrap_buildcache-{uuid.uuid4()}"

    @staticmethod
    def _spec_and_platform(
        abstract_spec_str: str,
    ) -> Tuple[spack.spec.Spec, spack.platforms.Platform]:
        """Return the spec object and platform we need to use when
        querying the buildcache.

        Args:
            abstract_spec_str: abstract spec string we are looking for
        """
        # Try to install from an unsigned binary cache
        abstract_spec = spack.spec.Spec(abstract_spec_str)
        # On Cray we want to use Linux binaries if available from mirrors
        bincache_platform = spack.platforms.real_host()
        return abstract_spec, bincache_platform

    def _read_metadata(self, package_name: str) -> Any:
        """Return metadata about the given package."""
        json_filename = f"{package_name}.json"
        json_dir = self.metadata_dir
        json_path = os.path.join(json_dir, json_filename)
        with open(json_path, encoding="utf-8") as stream:
            data = json.load(stream)
        return data

    def _install_by_hash(
        self, pkg_hash: str, pkg_sha256: str, bincache_platform: spack.platforms.Platform
    ) -> None:
        with spack.platforms.use_platform(bincache_platform):
            query = spack.binary_distribution.BinaryCacheQuery(all_architectures=True)
            for match in spack.store.find([f"/{pkg_hash}"], multiple=False, query_fn=query):
                spack.binary_distribution.install_root_node(
                    match, unsigned=True, force=True, sha256=pkg_sha256
                )

    def _install_and_test(
        self,
        abstract_spec: spack.spec.Spec,
        bincache_platform: spack.platforms.Platform,
        bincache_data,
        test_fn,
    ) -> bool:
        # Ensure we see only the buildcache being used to bootstrap
        with spack.config.override(self.mirror_scope):
            # This index is currently needed to get the compiler used to build some
            # specs that we know by dag hash.
            spack.binary_distribution.BINARY_INDEX.regenerate_spec_cache()
            index = spack.binary_distribution.update_cache_and_get_specs()

            if not index:
                raise RuntimeError("The binary index is empty")

            for item in bincache_data["verified"]:
                candidate_spec = item["spec"]
                # This will be None for things that don't depend on python
                python_spec = item.get("python", None)
                # Skip specs which are not compatible
                if not abstract_spec.intersects(candidate_spec):
                    continue

                if python_spec is not None and not abstract_spec.intersects(f"^{python_spec}"):
                    continue

                for _, pkg_hash, pkg_sha256 in item["binaries"]:
                    self._install_by_hash(pkg_hash, pkg_sha256, bincache_platform)

                info: ConfigDictionary = {}
                if test_fn(query_spec=abstract_spec, query_info=info):
                    self.last_search = info
                    return True
        return False

    def try_import(self, module: str, abstract_spec_str: str) -> bool:
        info: ConfigDictionary
        test_fn, info = functools.partial(_try_import_from_store, module), {}
        if test_fn(query_spec=abstract_spec_str, query_info=info):
            return True

        tty.debug(f"Bootstrapping {module} from pre-built binaries")
        abstract_spec, bincache_platform = self._spec_and_platform(
            abstract_spec_str + " ^" + spec_for_current_python()
        )
        data = self._read_metadata(module)
        return self._install_and_test(abstract_spec, bincache_platform, data, test_fn)

    def try_search_path(self, executables: Tuple[str], abstract_spec_str: str) -> bool:
        info: ConfigDictionary
        test_fn, info = functools.partial(_executables_in_store, executables), {}
        if test_fn(query_spec=abstract_spec_str, query_info=info):
            self.last_search = info
            return True

        abstract_spec, bincache_platform = self._spec_and_platform(abstract_spec_str)
        tty.debug(f"Bootstrapping {abstract_spec.name} from pre-built binaries")
        data = self._read_metadata(abstract_spec.name)
        return self._install_and_test(abstract_spec, bincache_platform, data, test_fn)


@bootstrapper(bootstrapper_type="install")
class SourceBootstrapper(Bootstrapper):
    """Install the software needed during bootstrapping from sources."""

    def __init__(self, conf) -> None:
        super().__init__(conf)
        self.last_search: Optional[ConfigDictionary] = None
        self.config_scope_name = f"bootstrap_source-{uuid.uuid4()}"

    def try_import(self, module: str, abstract_spec_str: str) -> bool:
        info: ConfigDictionary = {}
        if _try_import_from_store(module, abstract_spec_str, query_info=info):
            self.last_search = info
            return True

        tty.debug(f"Bootstrapping {module} from sources")

        # If we compile code from sources detecting a few build tools
        # might reduce compilation time by a fair amount
        _add_externals_if_missing()

        # Try to build and install from sources
        with spack_python_interpreter():
            if module == "clingo":
                bootstrapper = ClingoBootstrapConcretizer(configuration=spack.config.CONFIG)
                concrete_spec = bootstrapper.concretize()
            else:
                concrete_spec = spack.spec.Spec(
                    abstract_spec_str + " ^" + spec_for_current_python()
                )
                concrete_spec.concretize()

        msg = "[BOOTSTRAP MODULE {0}] Try installing '{1}' from sources"
        tty.debug(msg.format(module, abstract_spec_str))

        # Install the spec that should make the module importable
        with spack.config.override(self.mirror_scope):
            PackageInstaller([concrete_spec.package], fail_fast=True).install()

        if _try_import_from_store(module, query_spec=concrete_spec, query_info=info):
            self.last_search = info
            return True
        return False

    def try_search_path(self, executables: Tuple[str], abstract_spec_str: str) -> bool:
        info: ConfigDictionary = {}
        if _executables_in_store(executables, abstract_spec_str, query_info=info):
            self.last_search = info
            return True

        tty.debug(f"Bootstrapping {abstract_spec_str} from sources")

        # If we compile code from sources detecting a few build tools
        # might reduce compilation time by a fair amount
        _add_externals_if_missing()

        concrete_spec = spack.spec.Spec(abstract_spec_str).concretized()
        msg = "[BOOTSTRAP] Try installing '{0}' from sources"
        tty.debug(msg.format(abstract_spec_str))
        with spack.config.override(self.mirror_scope):
            PackageInstaller([concrete_spec.package], fail_fast=True).install()
        if _executables_in_store(executables, concrete_spec, query_info=info):
            self.last_search = info
            return True
        return False


def create_bootstrapper(conf: ConfigDictionary):
    """Return a bootstrap object built according to the configuration argument"""
    btype = conf["type"]
    return _bootstrap_methods[btype](conf)


def source_is_enabled_or_raise(conf: ConfigDictionary):
    """Raise ValueError if the source is not enabled for bootstrapping"""
    trusted, name = spack.config.get("bootstrap:trusted"), conf["name"]
    if not trusted.get(name, False):
        raise ValueError("source is not trusted")


def ensure_module_importable_or_raise(module: str, abstract_spec: Optional[str] = None):
    """Make the requested module available for import, or raise.

    This function tries to import a Python module in the current interpreter
    using, in order, the methods configured in bootstrap.yaml.

    If none of the methods succeed, an exception is raised. The function exits
    on first success.

    Args:
        module: module to be imported in the current interpreter
        abstract_spec: abstract spec that might provide the module. If not
            given it defaults to "module"

    Raises:
        ImportError: if the module couldn't be imported
    """
    # If we can import it already, that's great
    tty.debug(f"[BOOTSTRAP MODULE {module}] Try importing from Python")
    if _python_import(module):
        return

    abstract_spec = abstract_spec or module

    exception_handler = GroupedExceptionHandler()

    for current_config in bootstrapping_sources():
        with exception_handler.forward(current_config["name"], Exception):
            source_is_enabled_or_raise(current_config)
            current_bootstrapper = create_bootstrapper(current_config)
            if current_bootstrapper.try_import(module, abstract_spec):
                return

    assert exception_handler, (
        f"expected at least one exception to have been raised at this point: "
        f"while bootstrapping {module}"
    )
    msg = f'cannot bootstrap the "{module}" Python module '
    if abstract_spec:
        msg += f'from spec "{abstract_spec}" '
    if tty.is_debug():
        msg += exception_handler.grouped_message(with_tracebacks=True)
    else:
        msg += exception_handler.grouped_message(with_tracebacks=False)
        msg += "\nRun `spack --debug ...` for more detailed errors"
    raise ImportError(msg)


def ensure_executables_in_path_or_raise(
    executables: list,
    abstract_spec: str,
    cmd_check: Optional[Callable[[spack.util.executable.Executable], bool]] = None,
):
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

    exception_handler = GroupedExceptionHandler()

    for current_config in bootstrapping_sources():
        with exception_handler.forward(current_config["name"], Exception):
            source_is_enabled_or_raise(current_config)
            current_bootstrapper = create_bootstrapper(current_config)
            if current_bootstrapper.try_search_path(executables, abstract_spec):
                # Additional environment variables needed
                concrete_spec, cmd = (
                    current_bootstrapper.last_search["spec"],
                    current_bootstrapper.last_search["command"],
                )
                cmd.add_default_envmod(
                    spack.user_environment.environment_modifications_for_specs(
                        concrete_spec, set_package_py_globals=False
                    )
                )
                return cmd

    assert exception_handler, (
        f"expected at least one exception to have been raised at this point: "
        f"while bootstrapping {executables_str}"
    )
    msg = f"cannot bootstrap any of the {executables_str} executables "
    if abstract_spec:
        msg += f'from spec "{abstract_spec}" '
    if tty.is_debug():
        msg += exception_handler.grouped_message(with_tracebacks=True)
    else:
        msg += exception_handler.grouped_message(with_tracebacks=False)
        msg += "\nRun `spack --debug ...` for more detailed errors"
    raise RuntimeError(msg)


def _add_externals_if_missing() -> None:
    search_list = [
        # clingo
        "cmake",
        "bison",
        # GnuPG
        "gawk",
        # develop deps
        "git",
    ]
    if IS_WINDOWS:
        search_list.append("winbison")
    externals = spack.detection.by_path(search_list)
    # System git is typically deprecated, so mark as non-buildable to force it as external
    non_buildable_externals = {k: externals.pop(k) for k in ("git",) if k in externals}
    spack.detection.update_configuration(externals, scope="bootstrap", buildable=True)
    spack.detection.update_configuration(
        non_buildable_externals, scope="bootstrap", buildable=False
    )


def clingo_root_spec() -> str:
    """Return the root spec used to bootstrap clingo"""
    return _root_spec("clingo-bootstrap@spack+python")


def ensure_clingo_importable_or_raise() -> None:
    """Ensure that the clingo module is available for import."""
    ensure_module_importable_or_raise(module="clingo", abstract_spec=clingo_root_spec())


def gnupg_root_spec() -> str:
    """Return the root spec used to bootstrap GnuPG"""
    root_spec_name = "win-gpg" if IS_WINDOWS else "gnupg"
    return _root_spec(f"{root_spec_name}@2.3:")


def ensure_gpg_in_path_or_raise() -> None:
    """Ensure gpg or gpg2 are in the PATH or raise."""
    return ensure_executables_in_path_or_raise(
        executables=["gpg2", "gpg"], abstract_spec=gnupg_root_spec()
    )


def file_root_spec() -> str:
    """Return the root spec used to bootstrap file"""
    root_spec_name = "win-file" if IS_WINDOWS else "file"
    return _root_spec(root_spec_name)


def ensure_file_in_path_or_raise() -> None:
    """Ensure file is in the PATH or raise"""
    return ensure_executables_in_path_or_raise(
        executables=["file"], abstract_spec=file_root_spec()
    )


def patchelf_root_spec() -> str:
    """Return the root spec used to bootstrap patchelf"""
    # 0.13.1 is the last version not to require C++17.
    return _root_spec("patchelf@0.13.1:")


def verify_patchelf(patchelf: "spack.util.executable.Executable") -> bool:
    """Older patchelf versions can produce broken binaries, so we
    verify the version here.

    Arguments:

        patchelf: patchelf executable
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


def ensure_patchelf_in_path_or_raise() -> spack.util.executable.Executable:
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


def ensure_winsdk_external_or_raise() -> None:
    """Ensure the Windows SDK + WGL are available on system
    If both of these package are found, the Spack user or bootstrap
    configuration (depending on where Spack is running)
    will be updated to include all versions and variants detected.
    If either the WDK or WSDK are not found, this method will raise
    a RuntimeError.

    **NOTE:** This modifies the Spack config in the current scope,
    either user or environment depending on the calling context.
    This is different from all other current bootstrap dependency
    checks.
    """
    if set(["win-sdk", "wgl"]).issubset(spack.config.get("packages").keys()):
        return
    externals = spack.detection.by_path(["win-sdk", "wgl"])
    if not set(["win-sdk", "wgl"]) == externals.keys():
        missing_packages_lst = []
        if "wgl" not in externals:
            missing_packages_lst.append("wgl")
        if "win-sdk" not in externals:
            missing_packages_lst.append("win-sdk")
        missing_packages = " & ".join(missing_packages_lst)
        raise RuntimeError(
            f"Unable to find the {missing_packages}, please install these packages \
via the Visual Studio installer \
before proceeding with Spack or provide the path to a non standard install with \
'spack external find --path'"
        )
    # wgl/sdk are not required for bootstrapping Spack, but
    # are required for building anything non trivial
    # add to user config so they can be used by subsequent Spack ops
    spack.detection.update_configuration(externals, buildable=False)


def ensure_core_dependencies() -> None:
    """Ensure the presence of all the core dependencies."""
    if sys.platform.lower() == "linux":
        ensure_patchelf_in_path_or_raise()
    elif sys.platform == "win32":
        ensure_file_in_path_or_raise()
    ensure_gpg_in_path_or_raise()
    ensure_clingo_importable_or_raise()


def all_core_root_specs() -> List[str]:
    """Return a list of all the core root specs that may be used to bootstrap Spack"""
    return [clingo_root_spec(), gnupg_root_spec(), patchelf_root_spec(), file_root_spec()]


def bootstrapping_sources(scope: Optional[str] = None):
    """Return the list of configured sources of software for bootstrapping Spack

    Args:
        scope: if a valid configuration scope is given, return the
            list only from that scope
    """
    source_configs = spack.config.get("bootstrap:sources", default=None, scope=scope)
    source_configs = source_configs or []
    list_of_sources = []
    for entry in source_configs:
        current = copy.copy(entry)
        metadata_dir = spack.util.path.canonicalize_path(entry["metadata"])
        metadata_yaml = os.path.join(metadata_dir, METADATA_YAML_FILENAME)
        with open(metadata_yaml, encoding="utf-8") as stream:
            current.update(spack.util.spack_yaml.load(stream))
        list_of_sources.append(current)
    return list_of_sources
