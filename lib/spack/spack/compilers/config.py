# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This module contains functions related to finding compilers on the system,
and configuring Spack to use multiple compilers.
"""
import os
import re
import sys
import warnings
from typing import Any, Dict, List, Optional, Tuple

import archspec.cpu

import llnl.util.filesystem as fs
import llnl.util.lang
import llnl.util.tty as tty

import spack.config
import spack.detection
import spack.detection.path
import spack.error
import spack.platforms
import spack.repo
import spack.spec
from spack.operating_systems import windows_os
from spack.util.environment import get_path

package_name_to_compiler_name = {
    "llvm": "clang",
    "intel-oneapi-compilers": "oneapi",
    "llvm-amdgpu": "rocmcc",
    "intel-oneapi-compilers-classic": "intel",
    "acfl": "arm",
}


#: Tag used to identify packages providing a compiler
COMPILER_TAG = "compiler"


def compiler_config_files():
    config_files = []
    configuration = spack.config.CONFIG
    for scope in configuration.writable_scopes:
        name = scope.name

        from_packages_yaml = CompilerFactory.from_packages_yaml(configuration, scope=name)
        if from_packages_yaml:
            config_files.append(configuration.get_config_filename(name, "packages"))

        compiler_config = configuration.get("compilers", scope=name)
        if compiler_config:
            config_files.append(configuration.get_config_filename(name, "compilers"))

    return config_files


def add_compiler_to_config(new_compilers, *, scope=None) -> None:
    """Add a Compiler object to the configuration, at the required scope."""
    by_name: Dict[str, List["spack.spec.Spec"]] = {}
    for x in new_compilers:
        by_name.setdefault(x.name, []).append(x)

    spack.detection.update_configuration(by_name, buildable=True, scope=scope)


def find_compilers(
    path_hints: Optional[List[str]] = None,
    *,
    scope: Optional[str] = None,
    max_workers: Optional[int] = None,
) -> List["spack.spec.Spec"]:
    """Searches for compiler in the paths given as argument. If any new compiler is found, the
    configuration is updated, and the list of new compiler objects is returned.

    Args:
        path_hints: list of path hints where to look for. A sensible default based on the ``PATH``
            environment variable will be used if the value is None
        scope: configuration scope to modify
        max_workers: number of processes used to search for compilers
    """
    if path_hints is None:
        path_hints = get_path("PATH")
    default_paths = fs.search_paths_for_executables(*path_hints)
    if sys.platform == "win32":
        default_paths.extend(windows_os.WindowsOs().compiler_search_paths)
    compiler_pkgs = spack.repo.PATH.packages_with_tags(COMPILER_TAG, full=True)

    detected_packages = spack.detection.by_path(
        compiler_pkgs, path_hints=default_paths, max_workers=max_workers
    )

    new_compilers = spack.detection.update_configuration(
        detected_packages, buildable=True, scope=scope
    )
    return new_compilers


def select_new_compilers(
    candidates: List["spack.spec.Spec"], *, scope: Optional[str] = None
) -> List["spack.spec.Spec"]:
    """Given a list of compilers, remove those that are already defined in
    the configuration.
    """
    compilers_in_config = all_compilers_from(configuration=spack.config.CONFIG, scope=scope)
    return [c for c in candidates if c not in compilers_in_config]


def supported_compilers() -> List[str]:
    """Returns all the currently supported compiler packages"""
    return sorted(spack.repo.PATH.packages_with_tags(COMPILER_TAG))


def all_compilers(
    scope: Optional[str] = None, init_config: bool = True
) -> List["spack.spec.Spec"]:
    """Returns all the compilers from the current global configuration.

    Args:
        scope: configuration scope from which to extract the compilers. If None, the merged
            configuration is used.
        init_config: if True, search for compilers if none is found in configuration.
    """
    compilers = all_compilers_from(configuration=spack.config.CONFIG, scope=scope)

    if not compilers and init_config:
        _init_packages_yaml(spack.config.CONFIG, scope=scope)
        compilers = all_compilers_from(configuration=spack.config.CONFIG, scope=scope)

    return compilers


def _init_packages_yaml(
    configuration: "spack.config.ConfigurationType", *, scope: Optional[str]
) -> None:
    # Try importing from compilers.yaml
    legacy_compilers = CompilerFactory.from_compilers_yaml(configuration, scope=scope)
    if legacy_compilers:
        by_name: Dict[str, List[spack.spec.Spec]] = {}
        for legacy in legacy_compilers:
            by_name.setdefault(legacy.name, []).append(legacy)
        spack.detection.update_configuration(by_name, buildable=True, scope=scope)
        warnings.warn("compilers have been automatically converted from existing 'compilers.yaml'")
        return

    # Look for compilers in PATH
    new_compilers = find_compilers(scope=scope)
    if not new_compilers:
        raise NoAvailableCompilerError(
            "no compiler configured, and Spack cannot find working compilers in PATH"
        )
    warnings.warn("compilers have been configured automatically from PATH inspection")


def all_compilers_from(
    configuration: "spack.config.ConfigurationType", scope: Optional[str] = None
) -> List["spack.spec.Spec"]:
    """Returns all the compilers from the current global configuration.

    Args:
        configuration: configuration to be queried
        scope: configuration scope from which to extract the compilers. If None, the merged
            configuration is used.
    """
    compilers = CompilerFactory.from_packages_yaml(configuration, scope=scope)
    return compilers


class CompilerRemover:
    """Removes compiler from configuration."""

    def __init__(self, configuration: "spack.config.ConfigurationType") -> None:
        self.configuration = configuration
        self.marked_packages_yaml: List[Tuple[str, Any]] = []
        self.marked_compilers_yaml: List[Tuple[str, Any]] = []

    def mark_compilers(
        self, *, match: str, scope: Optional[str] = None
    ) -> List["spack.spec.Spec"]:
        """Marks compilers to be removed in configuration, and returns a corresponding list
        of specs.

        Args:
            match: constraint that the compiler must match to be removed.
            scope: scope where to remove the compiler. If None, all writeable scopes are checked.
        """
        self.marked_packages_yaml = []
        self.marked_compilers_yaml = []
        candidate_scopes = [scope]
        if scope is None:
            candidate_scopes = [x.name for x in self.configuration.writable_scopes]

        all_removals = self._mark_in_packages_yaml(match, candidate_scopes)
        all_removals.extend(self._mark_in_compilers_yaml(match, candidate_scopes))

        return all_removals

    def _mark_in_packages_yaml(self, match, candidate_scopes):
        compiler_package_names = supported_compilers()
        all_removals = []
        for current_scope in candidate_scopes:
            packages_yaml = self.configuration.get("packages", scope=current_scope)
            if not packages_yaml:
                continue

            removed_from_scope = []
            for name, entry in packages_yaml.items():
                if name not in compiler_package_names:
                    continue

                externals_config = entry.get("externals", None)
                if not externals_config:
                    continue

                def _partition_match(external_yaml):
                    s = CompilerFactory.from_external_yaml(external_yaml)
                    return not s.satisfies(match)

                to_keep, to_remove = llnl.util.lang.stable_partition(
                    externals_config, _partition_match
                )
                if not to_remove:
                    continue

                removed_from_scope.extend(to_remove)
                entry["externals"] = to_keep

            if not removed_from_scope:
                continue

            self.marked_packages_yaml.append((current_scope, packages_yaml))
            all_removals.extend(
                [CompilerFactory.from_external_yaml(x) for x in removed_from_scope]
            )
        return all_removals

    def _mark_in_compilers_yaml(self, match, candidate_scopes):
        if os.environ.get("SPACK_EXPERIMENTAL_DEPRECATE_COMPILERS_YAML") == "1":
            return []

        all_removals = []
        for current_scope in candidate_scopes:
            compilers_yaml = self.configuration.get("compilers", scope=current_scope)
            if not compilers_yaml:
                continue

            def _partition_match(entry):
                external_specs = CompilerFactory.from_legacy_yaml(entry["compiler"])
                return not any(x.satisfies(match) for x in external_specs)

            to_keep, to_remove = llnl.util.lang.stable_partition(compilers_yaml, _partition_match)
            if not to_remove:
                continue

            compilers_yaml[:] = to_keep
            self.marked_compilers_yaml.append((current_scope, compilers_yaml))
            for entry in to_remove:
                all_removals.extend(CompilerFactory.from_legacy_yaml(entry["compiler"]))

        return all_removals

    def flush(self):
        """Removes from configuration the specs that have been marked by the previous call
        of ``remove_compilers``.
        """
        for scope, packages_yaml in self.marked_packages_yaml:
            self.configuration.set("packages", packages_yaml, scope=scope)

        for scope, compilers_yaml in self.marked_compilers_yaml:
            self.configuration.set("compilers", compilers_yaml, scope=scope)


def compilers_for_arch(
    arch_spec: "spack.spec.ArchSpec", *, scope: Optional[str] = None
) -> List["spack.spec.Spec"]:
    """Returns the compilers that can be used on the input architecture"""
    compilers = all_compilers_from(spack.config.CONFIG, scope=scope)
    query = f"platform={arch_spec.platform} target=:{arch_spec.target}"
    return [x for x in compilers if x.satisfies(query)]


_EXTRA_ATTRIBUTES_KEY = "extra_attributes"
_COMPILERS_KEY = "compilers"
_C_KEY = "c"
_CXX_KEY, _FORTRAN_KEY = "cxx", "fortran"


def name_os_target(spec: "spack.spec.Spec") -> Tuple[str, str, str]:
    if not spec.architecture:
        host_platform = spack.platforms.host()
        operating_system = host_platform.operating_system("default_os")
        target = host_platform.target("default_target")
    else:
        target = spec.architecture.target
        if not target:
            target = spack.platforms.host().target("default_target")
        target = target

        operating_system = spec.os
        if not operating_system:
            host_platform = spack.platforms.host()
            operating_system = host_platform.operating_system("default_os")

    return spec.name, str(operating_system), str(target)


class CompilerFactory:
    """Class aggregating all ways of constructing a list of compiler specs from config entries."""

    _PACKAGES_YAML_CACHE: Dict[str, Optional["spack.spec.Spec"]] = {}
    _GENERIC_TARGET = None

    @staticmethod
    def from_packages_yaml(
        configuration: "spack.config.ConfigurationType", *, scope: Optional[str] = None
    ) -> List["spack.spec.Spec"]:
        """Returns the compiler specs defined in the "packages" section of the configuration"""
        compilers = []
        compiler_package_names = supported_compilers()
        packages_yaml = configuration.get("packages", scope=scope)
        for name, entry in packages_yaml.items():
            if name not in compiler_package_names:
                continue

            externals_config = entry.get("externals", None)
            if not externals_config:
                continue

            compiler_specs = []
            for current_external in externals_config:
                key = str(current_external)
                if key not in CompilerFactory._PACKAGES_YAML_CACHE:
                    CompilerFactory._PACKAGES_YAML_CACHE[key] = CompilerFactory.from_external_yaml(
                        current_external
                    )

                compiler = CompilerFactory._PACKAGES_YAML_CACHE[key]
                if compiler:
                    compiler_specs.append(compiler)

            compilers.extend(compiler_specs)
        return compilers

    @staticmethod
    def from_external_yaml(config: Dict[str, Any]) -> Optional["spack.spec.Spec"]:
        """Returns a compiler spec from an external definition from packages.yaml."""
        # Allow `@x.y.z` instead of `@=x.y.z`
        err_header = f"The external spec '{config['spec']}' cannot be used as a compiler"
        # If extra_attributes is not there I might not want to use this entry as a compiler,
        # therefore just leave a debug message, but don't be loud with a warning.
        if _EXTRA_ATTRIBUTES_KEY not in config:
            tty.debug(f"[{__file__}] {err_header}: missing the '{_EXTRA_ATTRIBUTES_KEY}' key")
            return None
        extra_attributes = config[_EXTRA_ATTRIBUTES_KEY]
        result = spack.spec.Spec(
            str(spack.spec.parse_with_version_concrete(config["spec"])),
            external_path=config.get("prefix"),
            external_modules=config.get("modules"),
        )
        result.extra_attributes = extra_attributes
        CompilerFactory._finalize_external_concretization(result)
        return result

    @staticmethod
    def _finalize_external_concretization(abstract_spec):
        if CompilerFactory._GENERIC_TARGET is None:
            CompilerFactory._GENERIC_TARGET = archspec.cpu.host().family

        if abstract_spec.architecture:
            abstract_spec.architecture.complete_with_defaults()
        else:
            abstract_spec.constrain(spack.spec.Spec.default_arch())
        abstract_spec.architecture.target = CompilerFactory._GENERIC_TARGET
        abstract_spec._finalize_concretization()

    @staticmethod
    def from_legacy_yaml(compiler_dict: Dict[str, Any]) -> List["spack.spec.Spec"]:
        """Returns a list of external specs, corresponding to a compiler entry
        from compilers.yaml.
        """
        # FIXME (compiler as nodes): should we look at targets too?
        result = []
        candidate_paths = [x for x in compiler_dict["paths"].values() if x is not None]
        finder = spack.detection.path.ExecutablesFinder()

        for pkg_name in spack.repo.PATH.packages_with_tags("compiler"):
            pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
            pattern = re.compile(r"|".join(finder.search_patterns(pkg=pkg_cls)))
            filtered_paths = [x for x in candidate_paths if pattern.search(os.path.basename(x))]
            detected = finder.detect_specs(pkg=pkg_cls, paths=filtered_paths)
            for s in detected:
                for key in ("flags", "environment", "extra_rpaths"):
                    if key in compiler_dict:
                        s.extra_attributes[key] = compiler_dict[key]

                if "modules" in compiler_dict:
                    s.external_modules = list(compiler_dict["modules"])

            result.extend(detected)

        # for item in result:
        #    CompilerFactory._finalize_external_concretization(item)

        return result

    @staticmethod
    def from_compilers_yaml(
        configuration: "spack.config.ConfigurationType", *, scope: Optional[str] = None
    ) -> List["spack.spec.Spec"]:
        """Returns the compiler specs defined in the "compilers" section of the configuration"""
        result: List["spack.spec.Spec"] = []
        for item in configuration.get("compilers", scope=scope):
            result.extend(CompilerFactory.from_legacy_yaml(item["compiler"]))
        return result


class UnknownCompilerError(spack.error.SpackError):
    def __init__(self, compiler_name):
        super().__init__(f"Spack doesn't support the requested compiler: {compiler_name}")


class NoAvailableCompilerError(spack.error.SpackError):
    pass
