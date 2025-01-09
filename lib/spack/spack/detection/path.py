# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Detection of software installed in the system, based on paths inspections
and running executables.
"""
import collections
import concurrent.futures
import os
import os.path
import re
import sys
import traceback
import warnings
from typing import Dict, Iterable, List, Optional, Set, Tuple, Type

import llnl.util.filesystem
import llnl.util.lang
import llnl.util.tty

import spack.error
import spack.spec
import spack.util.elf as elf_utils
import spack.util.environment
import spack.util.environment as environment
import spack.util.ld_so_conf
import spack.util.parallel

from .common import (
    WindowsCompilerExternalPaths,
    WindowsKitExternalPaths,
    _convert_to_iterable,
    compute_windows_program_path_for_package,
    compute_windows_user_path_for_package,
    executable_prefix,
    find_win32_additional_install_paths,
    library_prefix,
    path_to_dict,
)

#: Timeout used for package detection (seconds)
DETECTION_TIMEOUT = 60
if sys.platform == "win32":
    DETECTION_TIMEOUT = 120


def common_windows_package_paths(pkg_cls=None) -> List[str]:
    """Get the paths for common package installation location on Windows
    that are outside the PATH
    Returns [] on unix
    """
    if sys.platform != "win32":
        return []
    paths = WindowsCompilerExternalPaths.find_windows_compiler_bundled_packages()
    paths.extend(find_win32_additional_install_paths())
    paths.extend(WindowsKitExternalPaths.find_windows_kit_bin_paths())
    paths.extend(WindowsKitExternalPaths.find_windows_kit_reg_installed_roots_paths())
    paths.extend(WindowsKitExternalPaths.find_windows_kit_reg_sdk_paths())
    if pkg_cls:
        paths.extend(compute_windows_user_path_for_package(pkg_cls))
        paths.extend(compute_windows_program_path_for_package(pkg_cls))
    return paths


def file_identifier(path):
    s = os.stat(path)
    return s.st_dev, s.st_ino


def dedupe_paths(paths: List[str]) -> List[str]:
    """Deduplicate paths based on inode and device number. In case the list contains first a
    symlink and then the directory it points to, the symlink is replaced with the directory path.
    This ensures that we pick for example ``/usr/bin`` over ``/bin`` if the latter is a symlink to
    the former`."""
    seen: Dict[Tuple[int, int], str] = {}
    for path in paths:
        identifier = file_identifier(path)
        if identifier not in seen:
            seen[identifier] = path
        elif not os.path.islink(path):
            seen[identifier] = path
    return list(seen.values())


def executables_in_path(path_hints: List[str]) -> Dict[str, str]:
    """Get the paths of all executables available from the current PATH.

    For convenience, this is constructed as a dictionary where the keys are
    the executable paths and the values are the names of the executables
    (i.e. the basename of the executable path).

    There may be multiple paths with the same basename. In this case it is
    assumed there are two different instances of the executable.

    Args:
        path_hints: list of paths to be searched. If None the list will be
            constructed based on the PATH environment variable.
    """
    search_paths = llnl.util.filesystem.search_paths_for_executables(*path_hints)
    # Make use we don't doubly list /usr/lib and /lib etc
    return path_to_dict(dedupe_paths(search_paths))


def accept_elf(path, host_compat):
    """Accept an ELF file if the header matches the given compat triplet. In case it's not an ELF
    (e.g. static library, or some arbitrary file, fall back to is_readable_file)."""
    # Fast path: assume libraries at least have .so in their basename.
    # Note: don't replace with splitext, because of libsmth.so.1.2.3 file names.
    if ".so" not in os.path.basename(path):
        return llnl.util.filesystem.is_readable_file(path)
    try:
        return host_compat == elf_utils.get_elf_compat(path)
    except (OSError, elf_utils.ElfParsingError):
        return llnl.util.filesystem.is_readable_file(path)


def libraries_in_ld_and_system_library_path(
    path_hints: Optional[List[str]] = None,
) -> Dict[str, str]:
    """Get the paths of all libraries available from ``path_hints`` or the
    following defaults:

    - Environment variables (Linux: ``LD_LIBRARY_PATH``, Darwin: ``DYLD_LIBRARY_PATH``,
      and ``DYLD_FALLBACK_LIBRARY_PATH``)
    - Dynamic linker default paths (glibc: ld.so.conf, musl: ld-musl-<arch>.path)
    - Default system library paths.

    For convenience, this is constructed as a dictionary where the keys are
    the library paths and the values are the names of the libraries
    (i.e. the basename of the library path).

    There may be multiple paths with the same basename. In this case it is
    assumed there are two different instances of the library.

    Args:
        path_hints: list of paths to be searched. If None the list will be
            constructed based on the set of LD_LIBRARY_PATH, LIBRARY_PATH,
            DYLD_LIBRARY_PATH, and DYLD_FALLBACK_LIBRARY_PATH environment
            variables as well as the standard system library paths.
        path_hints (list): list of paths to be searched. If ``None``, the default
            system paths are used.
    """
    if path_hints:
        search_paths = llnl.util.filesystem.search_paths_for_libraries(*path_hints)
    else:
        search_paths = []

        # Environment variables
        if sys.platform == "darwin":
            search_paths.extend(environment.get_path("DYLD_LIBRARY_PATH"))
            search_paths.extend(environment.get_path("DYLD_FALLBACK_LIBRARY_PATH"))
        elif sys.platform.startswith("linux"):
            search_paths.extend(environment.get_path("LD_LIBRARY_PATH"))

        # Dynamic linker paths
        search_paths.extend(spack.util.ld_so_conf.host_dynamic_linker_search_paths())

        # Drop redundant paths
        search_paths = list(filter(os.path.isdir, search_paths))

    # Make use we don't doubly list /usr/lib and /lib etc
    search_paths = dedupe_paths(search_paths)

    try:
        host_compat = elf_utils.get_elf_compat(sys.executable)
        accept = lambda path: accept_elf(path, host_compat)
    except (OSError, elf_utils.ElfParsingError):
        accept = llnl.util.filesystem.is_readable_file

    path_to_lib = {}
    # Reverse order of search directories so that a lib in the first
    # search path entry overrides later entries
    for search_path in reversed(search_paths):
        for lib in os.listdir(search_path):
            lib_path = os.path.join(search_path, lib)
            if accept(lib_path):
                path_to_lib[lib_path] = lib
    return path_to_lib


def libraries_in_windows_paths(path_hints: Optional[List[str]] = None) -> Dict[str, str]:
    """Get the paths of all libraries available from the system PATH paths.

    For more details, see `libraries_in_ld_and_system_library_path` regarding
    return type and contents.

    Args:
        path_hints: list of paths to be searched. If None the list will be
            constructed based on the set of PATH environment
            variables as well as the standard system library paths.
    """
    search_hints = (
        path_hints if path_hints is not None else spack.util.environment.get_path("PATH")
    )
    search_paths = llnl.util.filesystem.search_paths_for_libraries(*search_hints)
    # on Windows, some libraries (.dlls) are found in the bin directory or sometimes
    # at the search root. Add both of those options to the search scheme
    search_paths.extend(llnl.util.filesystem.search_paths_for_executables(*search_hints))
    if path_hints is None:
        # if no user provided path was given, add defaults to the search
        search_paths.extend(WindowsKitExternalPaths.find_windows_kit_lib_paths())
        # SDK and WGL should be handled by above, however on occasion the WDK is in an atypical
        # location, so we handle that case specifically.
        search_paths.extend(WindowsKitExternalPaths.find_windows_driver_development_kit_paths())
    return path_to_dict(search_paths)


def _group_by_prefix(paths: List[str]) -> Dict[str, Set[str]]:
    groups = collections.defaultdict(set)
    for p in paths:
        groups[os.path.dirname(p)].add(p)
    return groups


class Finder:
    """Inspects the file-system looking for packages. Guesses places where to look using PATH."""

    def default_path_hints(self) -> List[str]:
        return []

    def search_patterns(self, *, pkg: Type["spack.package_base.PackageBase"]) -> List[str]:
        """Returns the list of patterns used to match candidate files.

        Args:
            pkg: package being detected
        """
        raise NotImplementedError("must be implemented by derived classes")

    def candidate_files(self, *, patterns: List[str], paths: List[str]) -> List[str]:
        """Returns a list of candidate files found on the system.

        Args:
            patterns: search patterns to be used for matching files
            paths: paths where to search for files
        """
        raise NotImplementedError("must be implemented by derived classes")

    def prefix_from_path(self, *, path: str) -> str:
        """Given a path where a file was found, returns the corresponding prefix.

        Args:
            path: path of a detected file
        """
        raise NotImplementedError("must be implemented by derived classes")

    def detect_specs(
        self, *, pkg: Type["spack.package_base.PackageBase"], paths: List[str]
    ) -> List["spack.spec.Spec"]:
        """Given a list of files matching the search patterns, returns a list of detected specs.

        Args:
            pkg: package being detected
            paths: files matching the package search patterns
        """
        if not hasattr(pkg, "determine_spec_details"):
            warnings.warn(
                f"{pkg.name} must define 'determine_spec_details' in order"
                f" for Spack to detect externally-provided instances"
                f" of the package."
            )
            return []

        result = []
        for candidate_path, items_in_prefix in _group_by_prefix(
            llnl.util.lang.dedupe(paths)
        ).items():
            # TODO: multiple instances of a package can live in the same
            # prefix, and a package implementation can return multiple specs
            # for one prefix, but without additional details (e.g. about the
            # naming scheme which differentiates them), the spec won't be
            # usable.
            try:
                specs = _convert_to_iterable(
                    pkg.determine_spec_details(candidate_path, items_in_prefix)
                )
            except Exception as e:
                specs = []
                if spack.error.SHOW_BACKTRACE:
                    details = traceback.format_exc()
                else:
                    details = f"[{e.__class__.__name__}: {e}]"
                warnings.warn(
                    f'error detecting "{pkg.name}" from prefix {candidate_path}: {details}'
                )

            if not specs:
                files = ", ".join(_convert_to_iterable(items_in_prefix))
                llnl.util.tty.debug(
                    f"The following files in {candidate_path} were decidedly not "
                    f"part of the package {pkg.name}: {files}"
                )

            resolved_specs: Dict[spack.spec.Spec, str] = {}  # spec -> exe found for the spec
            for spec in specs:
                prefix = self.prefix_from_path(path=candidate_path)
                if not prefix:
                    continue

                if spec in resolved_specs:
                    prior_prefix = ", ".join(_convert_to_iterable(resolved_specs[spec]))
                    llnl.util.tty.debug(
                        f"Files in {candidate_path} and {prior_prefix} are both associated"
                        f" with the same spec {str(spec)}"
                    )
                    continue

                resolved_specs[spec] = candidate_path
                try:
                    spec.validate_detection()
                except Exception as e:
                    msg = (
                        f'"{spec}" has been detected on the system but will '
                        f"not be added to packages.yaml [reason={str(e)}]"
                    )
                    warnings.warn(msg)
                    continue

                if not spec.external_path:
                    spec.external_path = prefix

                result.append(spec)

        return result

    def find(
        self, *, pkg_name: str, repository, initial_guess: Optional[List[str]] = None
    ) -> List["spack.spec.Spec"]:
        """For a given package, returns a list of detected specs.

        Args:
            pkg_name: package being detected
            repository: repository to retrieve the package
            initial_guess: initial list of paths to search from the caller if None, default paths
                are searched. If this is an empty list, nothing will be searched.
        """
        pkg_cls = repository.get_pkg_class(pkg_name)
        patterns = self.search_patterns(pkg=pkg_cls)
        if not patterns:
            return []
        if initial_guess is None:
            initial_guess = self.default_path_hints()
            initial_guess.extend(common_windows_package_paths(pkg_cls))
        candidates = self.candidate_files(patterns=patterns, paths=initial_guess)
        result = self.detect_specs(pkg=pkg_cls, paths=candidates)
        return result


class ExecutablesFinder(Finder):
    def default_path_hints(self) -> List[str]:
        return spack.util.environment.get_path("PATH")

    def search_patterns(self, *, pkg: Type["spack.package_base.PackageBase"]) -> List[str]:
        result = []
        if hasattr(pkg, "executables") and hasattr(pkg, "platform_executables"):
            result = pkg.platform_executables()
        return result

    def candidate_files(self, *, patterns: List[str], paths: List[str]) -> List[str]:
        executables_by_path = executables_in_path(path_hints=paths)
        joined_pattern = re.compile(r"|".join(patterns))
        result = [path for path, exe in executables_by_path.items() if joined_pattern.search(exe)]
        result.sort()
        return result

    def prefix_from_path(self, *, path: str) -> str:
        result = executable_prefix(path)
        if not result:
            msg = f"no bin/ dir found in {path}. Cannot add it as a Spack package"
            llnl.util.tty.debug(msg)
        return result


class LibrariesFinder(Finder):
    """Finds libraries on the system, searching by LD_LIBRARY_PATH, LIBRARY_PATH,
    DYLD_LIBRARY_PATH, DYLD_FALLBACK_LIBRARY_PATH, and standard system library paths
    """

    def search_patterns(self, *, pkg: Type["spack.package_base.PackageBase"]) -> List[str]:
        result = []
        if hasattr(pkg, "libraries"):
            result = pkg.libraries
        return result

    def candidate_files(self, *, patterns: List[str], paths: List[str]) -> List[str]:
        libraries_by_path = (
            libraries_in_ld_and_system_library_path(path_hints=paths)
            if sys.platform != "win32"
            else libraries_in_windows_paths(path_hints=paths)
        )
        patterns = [re.compile(x) for x in patterns]
        result = []
        for compiled_re in patterns:
            for path, exe in libraries_by_path.items():
                if compiled_re.search(exe):
                    result.append(path)
        return result

    def prefix_from_path(self, *, path: str) -> str:
        result = library_prefix(path)
        if not result:
            msg = f"no lib/ or lib64/ dir found in {path}. Cannot add it as a Spack package"
            llnl.util.tty.debug(msg)
        return result


def by_path(
    packages_to_search: Iterable[str],
    *,
    path_hints: Optional[List[str]] = None,
    max_workers: Optional[int] = None,
) -> Dict[str, List["spack.spec.Spec"]]:
    """Return the list of packages that have been detected on the system, keyed by
    unqualified package name.

    Args:
        packages_to_search: list of packages to be detected. Each package can be either unqualified
            of fully qualified
        path_hints: initial list of paths to be searched
        max_workers: maximum number of workers to search for packages in parallel
    """
    import spack.repo

    # TODO: Packages should be able to define both .libraries and .executables in the future
    # TODO: determine_spec_details should get all relevant libraries and executables in one call
    executables_finder, libraries_finder = ExecutablesFinder(), LibrariesFinder()
    detected_specs_by_package: Dict[str, Tuple[concurrent.futures.Future, ...]] = {}

    result = collections.defaultdict(list)
    repository = spack.repo.PATH.ensure_unwrapped()
    with spack.util.parallel.make_concurrent_executor(max_workers, require_fork=False) as executor:
        for pkg in packages_to_search:
            executable_future = executor.submit(
                executables_finder.find,
                pkg_name=pkg,
                initial_guess=path_hints,
                repository=repository,
            )
            library_future = executor.submit(
                libraries_finder.find,
                pkg_name=pkg,
                initial_guess=path_hints,
                repository=repository,
            )
            detected_specs_by_package[pkg] = executable_future, library_future

        for pkg_name, futures in detected_specs_by_package.items():
            for future in futures:
                try:
                    detected = future.result(timeout=DETECTION_TIMEOUT)
                    if detected:
                        _, unqualified_name = spack.repo.partition_package_name(pkg_name)
                        result[unqualified_name].extend(detected)
                except concurrent.futures.TimeoutError:
                    llnl.util.tty.debug(
                        f"[EXTERNAL DETECTION] Skipping {pkg_name}: timeout reached"
                    )
                except Exception:
                    llnl.util.tty.debug(
                        f"[EXTERNAL DETECTION] Skipping {pkg_name}: {traceback.format_exc()}"
                    )

    return result
