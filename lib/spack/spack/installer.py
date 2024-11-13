# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This module encapsulates package installation functionality.

The PackageInstaller coordinates concurrent builds of packages for the same
Spack instance by leveraging the dependency DAG and file system locks.  It
also proceeds with the installation of non-dependent packages of failed
dependencies in order to install as many dependencies of a package as possible.

Bottom-up traversal of the dependency DAG while prioritizing packages with no
uninstalled dependencies allows multiple processes to perform concurrent builds
of separate packages associated with a spec.

File system locks enable coordination such that no two processes attempt to
build the same or a failed dependency package.

If a dependency package fails to install, its dependents' tasks will be
removed from the installing process's queue.  A failure file is also written
and locked. Other processes use this file to detect the failure and dequeue
its dependents.

This module supports the coordination of local and distributed concurrent
installations of packages in a Spack instance.

"""

import copy
import enum
import glob
import heapq
import io
import itertools
import os
import shutil
import sys
import time
from collections import defaultdict
from gzip import GzipFile
from typing import Dict, Iterator, List, Optional, Set, Tuple, Union

import llnl.util.filesystem as fs
import llnl.util.lock as lk
import llnl.util.tty as tty
from llnl.string import ordinal
from llnl.util.lang import pretty_seconds
from llnl.util.tty.color import colorize
from llnl.util.tty.log import log_output

import spack.binary_distribution as binary_distribution
import spack.build_environment
import spack.config
import spack.database
import spack.deptypes as dt
import spack.error
import spack.hooks
import spack.mirror
import spack.package_base
import spack.package_prefs as prefs
import spack.repo
import spack.rewiring
import spack.spec
import spack.store
import spack.util.executable
import spack.util.path
import spack.util.timer as timer
from spack.util.environment import EnvironmentModifications, dump_environment
from spack.util.executable import which

#: Counter to support unique spec sequencing that is used to ensure packages
#: with the same priority are (initially) processed in the order in which they
#: were added (see https://docs.python.org/2/library/heapq.html).
_counter = itertools.count(0)


class BuildStatus(enum.Enum):
    """Different build (task) states."""

    #: Build status indicating task has been added/queued.
    QUEUED = enum.auto()

    #: Build status indicating the spec failed to install
    FAILED = enum.auto()

    #: Build status indicating the spec is being installed (possibly by another
    #: process)
    INSTALLING = enum.auto()

    #: Build status indicating the spec was sucessfully installed
    INSTALLED = enum.auto()

    #: Build status indicating the task has been popped from the queue
    DEQUEUED = enum.auto()

    #: Build status indicating task has been removed (to maintain priority
    #: queue invariants).
    REMOVED = enum.auto()

    def __str__(self):
        return f"{self.name.lower()}"


def _write_timer_json(pkg, timer, cache):
    extra_attributes = {"name": pkg.name, "cache": cache, "hash": pkg.spec.dag_hash()}
    try:
        with open(pkg.times_log_path, "w") as timelog:
            timer.write_json(timelog, extra_attributes=extra_attributes)
    except Exception as e:
        tty.debug(str(e))
        return


class ExecuteResult(enum.Enum):
    # Task succeeded
    SUCCESS = enum.auto()
    # Task failed
    FAILED = enum.auto()
    # Task is missing build spec and will be requeued
    MISSING_BUILD_SPEC = enum.auto()


class InstallAction(enum.Enum):
    #: Don't perform an install
    NONE = enum.auto()
    #: Do a standard install
    INSTALL = enum.auto()
    #: Do an overwrite install
    OVERWRITE = enum.auto()


class InstallStatus:
    def __init__(self, pkg_count: int):
        # Counters used for showing status information
        self.pkg_num: int = 0
        self.pkg_count: int = pkg_count
        self.pkg_ids: Set[str] = set()

    def next_pkg(self, pkg: "spack.package_base.PackageBase"):
        pkg_id = package_id(pkg.spec)

        if pkg_id not in self.pkg_ids:
            self.pkg_num += 1
            self.pkg_ids.add(pkg_id)

    def set_term_title(self, text: str):
        if not spack.config.get("config:install_status", True):
            return

        if not sys.stdout.isatty():
            return

        status = f"{text} {self.get_progress()}"
        sys.stdout.write(f"\x1b]0;Spack: {status}\x07")
        sys.stdout.flush()

    def get_progress(self) -> str:
        return f"[{self.pkg_num}/{self.pkg_count}]"


class TermStatusLine:
    """
    This class is used in distributed builds to inform the user that other packages are
    being installed by another process.
    """

    def __init__(self, enabled: bool):
        self.enabled: bool = enabled
        self.pkg_set: Set[str] = set()
        self.pkg_list: List[str] = []

    def add(self, pkg_id: str):
        """Add a package to the waiting list, and if it is new, update the status line."""
        if not self.enabled or pkg_id in self.pkg_set:
            return

        self.pkg_set.add(pkg_id)
        self.pkg_list.append(pkg_id)
        tty.msg(colorize("@*{Waiting for} @*g{%s}" % pkg_id))
        sys.stdout.flush()

    def clear(self):
        """Clear the status line."""
        if not self.enabled:
            return

        lines = len(self.pkg_list)

        if lines == 0:
            return

        self.pkg_set.clear()
        self.pkg_list = []

        # Move the cursor to the beginning of the first "Waiting for" message and clear
        # everything after it.
        sys.stdout.write(f"\x1b[{lines}F\x1b[J")
        sys.stdout.flush()


def _check_last_phase(pkg: "spack.package_base.PackageBase") -> None:
    """
    Ensures the specified package has a valid last phase before proceeding
    with its installation.

    The last phase is also set to None if it is the last phase of the
    package already.

    Args:
        pkg: the package being installed

    Raises:
        ``BadInstallPhase`` if stop_before or last phase is invalid
    """
    phases = pkg.builder.phases  # type: ignore[attr-defined]
    if pkg.stop_before_phase and pkg.stop_before_phase not in phases:  # type: ignore[attr-defined]
        raise BadInstallPhase(pkg.name, pkg.stop_before_phase)  # type: ignore[attr-defined]

    if pkg.last_phase and pkg.last_phase not in phases:  # type: ignore[attr-defined]
        raise BadInstallPhase(pkg.name, pkg.last_phase)  # type: ignore[attr-defined]

    # If we got a last_phase, make sure it's not already last
    if pkg.last_phase and pkg.last_phase == phases[-1]:  # type: ignore[attr-defined]
        pkg.last_phase = None  # type: ignore[attr-defined]


def _handle_external_and_upstream(pkg: "spack.package_base.PackageBase", explicit: bool) -> bool:
    """
    Determine if the package is external or upstream and register it in the
    database if it is external package.

    Args:
        pkg: the package whose installation is under consideration
        explicit: the package was explicitly requested by the user
    Return:
        ``True`` if the package is not to be installed locally, otherwise ``False``
    """
    # For external packages the workflow is simplified, and basically
    # consists in module file generation and registration in the DB.
    if pkg.spec.external:
        _process_external_package(pkg, explicit)
        _print_installed_pkg(f"{pkg.prefix} (external {package_id(pkg.spec)})")
        return True

    if pkg.spec.installed_upstream:
        tty.verbose(
            f"{package_id(pkg.spec)} is installed in an upstream Spack instance at "
            f"{pkg.spec.prefix}"
        )
        _print_installed_pkg(pkg.prefix)

        # This will result in skipping all post-install hooks. In the case
        # of modules this is considered correct because we want to retrieve
        # the module from the upstream Spack instance.
        return True

    return False


def _do_fake_install(pkg: "spack.package_base.PackageBase") -> None:
    """Make a fake install directory with fake executables, headers, and libraries."""
    command = pkg.name
    header = pkg.name
    library = pkg.name

    # Avoid double 'lib' for packages whose names already start with lib
    if not pkg.name.startswith("lib"):
        library = "lib" + library

    plat_shared = ".dll" if sys.platform == "win32" else ".so"
    plat_static = ".lib" if sys.platform == "win32" else ".a"
    dso_suffix = ".dylib" if sys.platform == "darwin" else plat_shared

    # Install fake command
    fs.mkdirp(pkg.prefix.bin)
    fs.touch(os.path.join(pkg.prefix.bin, command))
    if sys.platform != "win32":
        chmod = which("chmod")
        chmod("+x", os.path.join(pkg.prefix.bin, command))

    # Install fake header file
    fs.mkdirp(pkg.prefix.include)
    fs.touch(os.path.join(pkg.prefix.include, header + ".h"))

    # Install fake shared and static libraries
    fs.mkdirp(pkg.prefix.lib)
    for suffix in [dso_suffix, plat_static]:
        fs.touch(os.path.join(pkg.prefix.lib, library + suffix))

    # Install fake man page
    fs.mkdirp(pkg.prefix.man.man1)

    packages_dir = spack.store.STORE.layout.build_packages_path(pkg.spec)
    dump_packages(pkg.spec, packages_dir)


def _hms(seconds: int) -> str:
    """
    Convert seconds to hours, minutes, seconds

    Args:
        seconds: time to be converted in seconds

    Return: String representation of the time as #h #m #.##s
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    parts = []
    if h:
        parts.append("%dh" % h)
    if m:
        parts.append("%dm" % m)
    if s:
        parts.append(f"{s:.2f}s")
    return " ".join(parts)


def _log_prefix(pkg_name) -> str:
    """Prefix of the form "[pid]: [pkg name]: ..." when printing a status update during
    the build."""
    pid = f"{os.getpid()}: " if tty.show_pid() else ""
    return f"{pid}{pkg_name}:"


def _print_installed_pkg(message: str) -> None:
    """
    Output a message with a package icon.

    Args:
        message (str): message to be output
    """
    if tty.msg_enabled():
        print(colorize("@*g{[+]} ") + spack.util.path.debug_padded_filter(message))


def print_install_test_log(pkg: "spack.package_base.PackageBase") -> None:
    """Output install test log file path but only if have test failures.

    Args:
        pkg: instance of the package under test
    """
    if not pkg.run_tests or not (pkg.tester and pkg.tester.test_failures):
        # The tests were not run or there were no test failures
        return

    pkg.tester.print_log_path()


def _print_timer(pre: str, pkg_id: str, timer: timer.BaseTimer) -> None:
    phases = [f"{p.capitalize()}: {_hms(timer.duration(p))}." for p in timer.phases]
    phases.append(f"Total: {_hms(timer.duration())}")
    tty.msg(f"{pre} Successfully installed {pkg_id}", "  ".join(phases))


def _install_from_cache(
    pkg: "spack.package_base.PackageBase", explicit: bool, unsigned: Optional[bool] = False
) -> bool:
    """
    Install the package from binary cache

    Args:
        pkg: package to install from the binary cache
        explicit: ``True`` if installing the package was explicitly
            requested by the user, otherwise, ``False``
        unsigned: if ``True`` or ``False`` override the mirror signature verification defaults

    Return: ``True`` if the package was extract from binary cache, ``False`` otherwise
    """
    t = timer.Timer()
    installed_from_cache = _try_install_from_binary_cache(
        pkg, explicit, unsigned=unsigned, timer=t
    )
    if not installed_from_cache:
        return False
    t.stop()

    pkg_id = package_id(pkg.spec)
    tty.debug(f"Successfully extracted {pkg_id} from binary cache")

    _write_timer_json(pkg, t, True)
    _print_timer(pre=_log_prefix(pkg.name), pkg_id=pkg_id, timer=t)
    _print_installed_pkg(pkg.spec.prefix)
    spack.hooks.post_install(pkg.spec, explicit)
    return True


def _process_external_package(pkg: "spack.package_base.PackageBase", explicit: bool) -> None:
    """
    Helper function to run post install hooks and register external packages.

    Args:
        pkg: the external package
        explicit: if the package was requested explicitly by the user,
            ``False`` if it was pulled in as a dependency of an explicit
            package.
    """
    assert pkg.spec.external, "Expected to post-install/register an external package."

    pre = f"{pkg.spec.name}@{pkg.spec.version} :"
    spec = pkg.spec

    if spec.external_modules:
        tty.msg(f"{pre} has external module in {spec.external_modules}")
        tty.debug(f"{pre} is actually installed in {spec.external_path}")
    else:
        tty.debug(f"{pre} externally installed in {spec.external_path}")

    try:
        # Check if the package was already registered in the DB.
        # If this is the case, then only make explicit if required.
        tty.debug(f"{pre} already registered in DB")
        record = spack.store.STORE.db.get_record(spec)
        if explicit and not record.explicit:
            spack.store.STORE.db.update_explicit(spec, explicit)

    except KeyError:
        # If not, register it and generate the module file.
        # For external packages we just need to run
        # post-install hooks to generate module files.
        tty.debug(f"{pre} generating module file")
        spack.hooks.post_install(spec, explicit)

        # Add to the DB
        tty.debug(f"{pre} registering into DB")
        spack.store.STORE.db.add(spec, explicit=explicit)


def _process_binary_cache_tarball(
    pkg: "spack.package_base.PackageBase",
    explicit: bool,
    unsigned: Optional[bool],
    mirrors_for_spec: Optional[list] = None,
    timer: timer.BaseTimer = timer.NULL_TIMER,
) -> bool:
    """
    Process the binary cache tarball.

    Args:
        pkg: the package being installed
        explicit: the package was explicitly requested by the user
        unsigned: if ``True`` or ``False`` override the mirror signature verification defaults
        mirrors_for_spec: Optional list of concrete specs and mirrors
        obtained by calling binary_distribution.get_mirrors_for_spec().
        timer: timer to keep track of binary install phases.

    Return:
        bool: ``True`` if the package was extracted from binary cache,
            else ``False``
    """
    with timer.measure("fetch"):
        download_result = binary_distribution.download_tarball(
            pkg.spec.build_spec, unsigned, mirrors_for_spec
        )

        if download_result is None:
            return False

    tty.msg(f"Extracting {package_id(pkg.spec)} from binary cache")

    with timer.measure("install"), spack.util.path.filter_padding():
        binary_distribution.extract_tarball(pkg.spec, download_result, force=False, timer=timer)

        if pkg.spec.spliced:  # overwrite old metadata with new
            spack.store.STORE.layout.write_spec(
                pkg.spec, spack.store.STORE.layout.spec_file_path(pkg.spec)
            )

        if hasattr(pkg, "_post_buildcache_install_hook"):
            pkg._post_buildcache_install_hook()

        pkg.installed_from_binary_cache = True
        spack.store.STORE.db.add(pkg.spec, explicit=explicit)
        return True


def _try_install_from_binary_cache(
    pkg: "spack.package_base.PackageBase",
    explicit: bool,
    unsigned: Optional[bool] = None,
    timer: timer.BaseTimer = timer.NULL_TIMER,
) -> bool:
    """
    Try to extract the package from binary cache.

    Args:
        pkg: package to be extracted from binary cache
        explicit: the package was explicitly requested by the user
        unsigned: if ``True`` or ``False`` override the mirror signature verification defaults
        timer: timer to keep track of binary install phases.
    """
    # Early exit if no binary mirrors are configured.
    if not spack.mirror.MirrorCollection(binary=True):
        return False

    tty.debug(f"Searching for binary cache of {package_id(pkg.spec)}")

    with timer.measure("search"):
        matches = binary_distribution.get_mirrors_for_spec(pkg.spec, index_only=True)

    return _process_binary_cache_tarball(
        pkg, explicit, unsigned, mirrors_for_spec=matches, timer=timer
    )


def combine_phase_logs(phase_log_files: List[str], log_path: str) -> None:
    """
    Read set or list of logs and combine them into one file.

    Each phase will produce it's own log, so this function aims to cat all the
    separate phase log output files into the pkg.log_path. It is written
    generally to accept some list of files, and a log path to combine them to.

    Args:
        phase_log_files: a list or iterator of logs to combine
        log_path: the path to combine them to
    """
    with open(log_path, "bw") as log_file:
        for phase_log_file in phase_log_files:
            with open(phase_log_file, "br") as phase_log:
                shutil.copyfileobj(phase_log, log_file)


def dump_packages(spec: "spack.spec.Spec", path: str) -> None:
    """
    Dump all package information for a spec and its dependencies.

    This creates a package repository within path for every namespace in the
    spec DAG, and fills the repos with package files and patch files for every
    node in the DAG.

    Args:
        spec: the Spack spec whose package information is to be dumped
        path: the path to the build packages directory
    """
    fs.mkdirp(path)

    # Copy in package.py files from any dependencies.
    # Note that we copy them in as they are in the *install* directory
    # NOT as they are in the repository, because we want a snapshot of
    # how *this* particular build was done.
    for node in spec.traverse(deptype=all):
        if node is not spec:
            # Locate the dependency package in the install tree and find
            # its provenance information.
            source = spack.store.STORE.layout.build_packages_path(node)
            source_repo_root = os.path.join(source, node.namespace)

            # If there's no provenance installed for the package, skip it.
            # If it's external, skip it because it either:
            # 1) it wasn't built with Spack, so it has no Spack metadata
            # 2) it was built by another Spack instance, and we do not
            # (currently) use Spack metadata to associate repos with externals
            # built by other Spack instances.
            # Spack can always get something current from the builtin repo.
            if node.external or not os.path.isdir(source_repo_root):
                continue

            # Create a source repo and get the pkg directory out of it.
            try:
                source_repo = spack.repo.from_path(source_repo_root)
                source_pkg_dir = source_repo.dirname_for_package_name(node.name)
            except spack.repo.RepoError as err:
                tty.debug(f"Failed to create source repo for {node.name}: {str(err)}")
                source_pkg_dir = None
                tty.warn(f"Warning: Couldn't copy in provenance for {node.name}")

        # Create a destination repository
        dest_repo_root = os.path.join(path, node.namespace)
        if not os.path.exists(dest_repo_root):
            spack.repo.create_repo(dest_repo_root)
        repo = spack.repo.from_path(dest_repo_root)

        # Get the location of the package in the dest repo.
        dest_pkg_dir = repo.dirname_for_package_name(node.name)
        if node is spec:
            spack.repo.PATH.dump_provenance(node, dest_pkg_dir)
        elif source_pkg_dir:
            fs.install_tree(source_pkg_dir, dest_pkg_dir)


def get_dependent_ids(spec: "spack.spec.Spec") -> List[str]:
    """
    Return a list of package ids for the spec's dependents

    Args:
        spec: Concretized spec

    Returns: list of package ids
    """
    return [package_id(d) for d in spec.dependents()]


def install_msg(name: str, pid: int, install_status: InstallStatus) -> str:
    """
    Colorize the name/id of the package being installed

    Args:
        name: Name/id of the package being installed
        pid: id of the installer process

    Return: Colorized installing message
    """
    pre = f"{pid}: " if tty.show_pid() else ""
    post = (
        " @*{%s}" % install_status.get_progress()
        if install_status and spack.config.get("config:install_status", True)
        else ""
    )
    return pre + colorize("@*{Installing} @*g{%s}%s" % (name, post))


def archive_install_logs(pkg: "spack.package_base.PackageBase", phase_log_dir: str) -> None:
    """
    Copy install logs to their destination directory(ies)
    Args:
        pkg: the package that was built and installed
        phase_log_dir: path to the archive directory
    """
    # Copy a compressed version of the install log
    with open(pkg.log_path, "rb") as f, open(pkg.install_log_path, "wb") as g:
        # Use GzipFile directly so we can omit filename / mtime in header
        gzip_file = GzipFile(filename="", mode="wb", compresslevel=6, mtime=0, fileobj=g)
        shutil.copyfileobj(f, gzip_file)
        gzip_file.close()

    # Archive the install-phase test log, if present
    pkg.archive_install_test_log()


def log(pkg: "spack.package_base.PackageBase") -> None:
    """
    Copy provenance into the install directory on success

    Args:
        pkg: the package that was built and installed
    """
    packages_dir = spack.store.STORE.layout.build_packages_path(pkg.spec)

    # Remove first if we're overwriting another build
    try:
        # log and env install paths are inside this
        shutil.rmtree(packages_dir)
    except Exception as e:
        # FIXME : this potentially catches too many things...
        tty.debug(e)

    archive_install_logs(pkg, os.path.dirname(packages_dir))

    # Archive the environment modifications for the build.
    fs.install(pkg.env_mods_path, pkg.install_env_path)

    if os.path.exists(pkg.configure_args_path):
        # Archive the args used for the build
        fs.install(pkg.configure_args_path, pkg.install_configure_args_path)

    # Finally, archive files that are specific to each package
    with fs.working_dir(pkg.stage.path):
        errors = io.StringIO()
        target_dir = os.path.join(
            spack.store.STORE.layout.metadata_path(pkg.spec), "archived-files"
        )

        for glob_expr in pkg.builder.archive_files:
            # Check that we are trying to copy things that are
            # in the stage tree (not arbitrary files)
            abs_expr = os.path.realpath(glob_expr)
            if os.path.realpath(pkg.stage.path) not in abs_expr:
                errors.write(f"[OUTSIDE SOURCE PATH]: {glob_expr}\n")
                continue
            # Now that we are sure that the path is within the correct
            # folder, make it relative and check for matches
            if os.path.isabs(glob_expr):
                glob_expr = os.path.relpath(glob_expr, pkg.stage.path)
            files = glob.glob(glob_expr)
            for f in files:
                try:
                    target = os.path.join(target_dir, f)
                    # We must ensure that the directory exists before
                    # copying a file in
                    fs.mkdirp(os.path.dirname(target))
                    fs.install(f, target)
                except Exception as e:
                    tty.debug(e)

                    # Here try to be conservative, and avoid discarding
                    # the whole install procedure because of copying a
                    # single file failed
                    errors.write(f"[FAILED TO ARCHIVE]: {f}")

        if errors.getvalue():
            error_file = os.path.join(target_dir, "errors.txt")
            fs.mkdirp(target_dir)
            with open(error_file, "w") as err:
                err.write(errors.getvalue())
            tty.warn(f"Errors occurred when archiving files.\n\tSee: {error_file}")

    dump_packages(pkg.spec, packages_dir)


def package_id(spec: "spack.spec.Spec") -> str:
    """A "unique" package identifier for installation purposes

    The identifier is used to track tasks, locks, install, and
    failure statuses.

    The identifier needs to distinguish between combinations of compilers
    and packages for combinatorial environments.

    Args:
        pkg: the package from which the identifier is derived
    """
    if not spec.concrete:
        raise ValueError("Cannot provide a unique, readable id when the spec is not concretized.")

    return f"{spec.name}-{spec.version}-{spec.dag_hash()}"


class BuildRequest:
    """Class for representing an installation request."""

    def __init__(self, pkg: "spack.package_base.PackageBase", install_args: dict):
        """
        Instantiate a build request for a package.

        Args:
            pkg: the package to be built and installed
            install_args: the install arguments associated with ``pkg``
        """
        # Ensure dealing with a package that has a concrete spec
        if not isinstance(pkg, spack.package_base.PackageBase):
            raise ValueError(f"{str(pkg)} must be a package")

        self.pkg = pkg
        if not self.pkg.spec.concrete:
            raise ValueError(f"{self.pkg.name} must have a concrete spec")

        self.pkg.stop_before_phase = install_args.get("stop_before")  # type: ignore[attr-defined] # noqa: E501
        self.pkg.last_phase = install_args.get("stop_at")  # type: ignore[attr-defined]

        # Cache the package id for convenience
        self.pkg_id = package_id(pkg.spec)

        # Save off the original install arguments plus standard defaults
        # since they apply to the requested package *and* dependencies.
        self.install_args = install_args if install_args else {}
        self._add_default_args()

        # Cache overwrite information
        self.overwrite = set(self.install_args.get("overwrite", []))
        self.overwrite_time = time.time()

        # Save off dependency package ids for quick checks since traversals
        # are not able to return full dependents for all packages across
        # environment specs.
        self.dependencies = set(
            package_id(d)
            for d in self.pkg.spec.dependencies(deptype=self.get_depflags(self.pkg))
            if package_id(d) != self.pkg_id
        )

    def __repr__(self) -> str:
        """Return a formal representation of the build request."""
        rep = f"{self.__class__.__name__}("
        for attr, value in self.__dict__.items():
            rep += f"{attr}={value.__repr__()}, "
        return f"{rep.strip(', ')})"

    def __str__(self) -> str:
        """Return a printable version of the build request."""
        return f"package={self.pkg.name}, install_args={self.install_args}"

    def _add_default_args(self) -> None:
        """Ensure standard install options are set to at least the default."""
        for arg, default in [
            ("context", "build"),  # installs *always* build
            ("dependencies_cache_only", False),
            ("dependencies_use_cache", True),
            ("dirty", False),
            ("fail_fast", False),
            ("fake", False),
            ("install_deps", True),
            ("install_package", True),
            ("install_source", False),
            ("package_cache_only", False),
            ("package_use_cache", True),
            ("keep_prefix", False),
            ("keep_stage", False),
            ("restage", False),
            ("skip_patch", False),
            ("tests", False),
            ("unsigned", None),
            ("verbose", False),
        ]:
            _ = self.install_args.setdefault(arg, default)

    def get_depflags(self, pkg: "spack.package_base.PackageBase") -> int:
        """Determine the required dependency types for the associated package.

        Args:
            pkg: explicit or implicit package being installed

        Returns:
            tuple: required dependency type(s) for the package
        """
        depflag = dt.LINK | dt.RUN
        include_build_deps = self.install_args.get("include_build_deps")

        if self.pkg_id == package_id(pkg.spec):
            cache_only = self.install_args.get("package_cache_only")
        else:
            cache_only = self.install_args.get("dependencies_cache_only")

        # Include build dependencies if pkg is going to be built from sources, or
        # if build deps are explicitly requested.
        if include_build_deps or not (
            cache_only or pkg.spec.installed and not pkg.spec.dag_hash() in self.overwrite
        ):
            depflag |= dt.BUILD
        if self.run_tests(pkg):
            depflag |= dt.TEST
        return depflag

    def has_dependency(self, dep_id) -> bool:
        """Returns ``True`` if the package id represents a known dependency
        of the requested package, ``False`` otherwise."""
        return dep_id in self.dependencies

    def run_tests(self, pkg: "spack.package_base.PackageBase") -> bool:
        """Determine if the tests should be run for the provided packages

        Args:
            pkg: explicit or implicit package being installed

        Returns:
            bool: ``True`` if they should be run; ``False`` otherwise
        """
        tests = self.install_args.get("tests", False)
        return tests is True or (tests and pkg.name in tests)

    @property
    def spec(self) -> "spack.spec.Spec":
        """The specification associated with the package."""
        return self.pkg.spec

    def traverse_dependencies(self, spec=None, visited=None) -> Iterator["spack.spec.Spec"]:
        """Yield any dependencies of the appropriate type(s)"""
        # notice: deptype is not constant across nodes, so we cannot use
        # spec.traverse_edges(deptype=...).

        if spec is None:
            spec = self.spec
        if visited is None:
            visited = set()

        for dep in spec.dependencies(deptype=self.get_depflags(spec.package)):
            hash = dep.dag_hash()
            if hash in visited:
                continue
            visited.add(hash)
            # In Python 3: yield from self.traverse_dependencies(dep, visited)
            for s in self.traverse_dependencies(dep, visited):
                yield s
            yield dep


class Task:
    """Base class for representing a task for a package."""

    def __init__(
        self,
        pkg: "spack.package_base.PackageBase",
        request: BuildRequest,
        *,
        compiler: bool = False,
        start: float = 0.0,
        attempts: int = 0,
        status: BuildStatus = BuildStatus.QUEUED,
        installed: Set[str] = set(),
    ):
        """
        Instantiate a task for a package.

        Args:
            pkg: the package to be built and installed
            request: the associated install request
            start: the initial start time for the package, in seconds
            attempts: the number of attempts to install the package, which
                should be 0 when the task is initially instantiated
            status: the installation status
            installed: the (string) identifiers of packages that have
                been installed so far

        Raises:
            ``InstallError`` if the build status is incompatible with the task
            ``TypeError`` if provided an argument of the wrong type
            ``ValueError`` if provided an argument with the wrong value or state
        """

        # Ensure dealing with a package that has a concrete spec
        if not isinstance(pkg, spack.package_base.PackageBase):
            raise TypeError(f"{str(pkg)} must be a package")

        self.pkg = pkg
        if not self.pkg.spec.concrete:
            raise ValueError(f"{self.pkg.name} must have a concrete spec")

        # The "unique" identifier for the task's package
        self.pkg_id = package_id(self.pkg.spec)

        # The explicit build request associated with the package
        if not isinstance(request, BuildRequest):
            raise TypeError(f"{request} is not a valid build request")
        self.request = request

        # Initialize the status to an active state.  The status is used to
        # ensure priority queue invariants when tasks are "removed" from the
        # queue.
        if not isinstance(status, BuildStatus):
            raise TypeError(f"{status} is not a valid build status")

        # The initial build task cannot have status "removed".
        if attempts == 0 and status == BuildStatus.REMOVED:
            raise spack.error.InstallError(
                f"Cannot create a task for {self.pkg_id} with status '{status}'", pkg=pkg
            )
        self.status = status

        # cache the PID, which is used for distributed build messages in self.execute
        self.pid = os.getpid()

        # The initial start time for processing the spec
        self.start = start

        if not isinstance(installed, set):
            raise TypeError(
                f"BuildTask constructor requires 'installed' be a 'set', "
                f"not '{installed.__class__.__name__}'."
            )

        # Set of dependents, which needs to include the requesting package
        # to support tracking of parallel, multi-spec, environment installs.
        self.dependents = set(get_dependent_ids(self.pkg.spec))

        tty.debug(f"Pkg id {self.pkg_id} has the following dependents:")
        for dep_id in self.dependents:
            tty.debug(f"- {dep_id}")

        # Set of dependencies
        #
        # Be consistent wrt use of dependents and dependencies.  That is,
        # if use traverse for transitive dependencies, then must remove
        # transitive dependents on failure.
        self.dependencies = set(
            package_id(d)
            for d in self.pkg.spec.dependencies(deptype=self.request.get_depflags(self.pkg))
            if package_id(d) != self.pkg_id
        )

        # List of uninstalled dependencies, which is used to establish
        # the priority of the task.
        self.uninstalled_deps = set(
            pkg_id for pkg_id in self.dependencies if pkg_id not in installed
        )

        # Ensure key sequence-related properties are updated accordingly.
        self.attempts = attempts
        self._update()

    def execute(self, install_status: InstallStatus) -> ExecuteResult:
        """Execute the work of this task.

        The ``install_status`` is an ``InstallStatus`` object used to format progress reporting for
        this task in the context of the full ``BuildRequest``."""
        raise NotImplementedError

    def __eq__(self, other):
        return self.key == other.key

    def __ge__(self, other):
        return self.key >= other.key

    def __gt__(self, other):
        return self.key > other.key

    def __le__(self, other):
        return self.key <= other.key

    def __lt__(self, other):
        return self.key < other.key

    def __ne__(self, other):
        return self.key != other.key

    def __repr__(self) -> str:
        """Returns a formal representation of the task."""
        rep = f"{self.__class__.__name__}("
        for attr, value in self.__dict__.items():
            rep += f"{attr}={value.__repr__()}, "
        return f"{rep.strip(', ')})"

    def __str__(self) -> str:
        """Returns a printable version of the task."""
        dependencies = f"#dependencies={len(self.dependencies)}"
        return "priority={0}, status={1}, start={2}, {3}".format(
            self.priority, self.status, self.start, dependencies
        )

    def _update(self) -> None:
        """Update properties associated with a new instance of a task."""
        # Number of times the task has/will be queued
        self.attempts = self.attempts + 1

        # Ensure the task gets a unique sequence number to preserve the
        # order in which it is added.
        self.sequence = next(_counter)

    def add_dependent(self, pkg_id: str) -> None:
        """
        Ensure the package is in this task's ``dependents`` list.

        Args:
            pkg_id:  package identifier of the dependent package
        """
        if pkg_id != self.pkg_id and pkg_id not in self.dependents:
            tty.debug(f"Adding {pkg_id} as a dependent of {self.pkg_id}")
            self.dependents.add(pkg_id)

    def add_dependency(self, pkg_id, installed=False):
        """
        Ensure the package is in this task's ``dependencies`` list.

        Args:
            pkg_id (str):  package identifier of the dependency package
            installed (bool):  install status of the dependency package
        """
        if pkg_id != self.pkg_id and pkg_id not in self.dependencies:
            tty.debug(f"Adding {pkg_id} as a depencency of {self.pkg_id}")
            self.dependencies.add(pkg_id)
            if not installed:
                self.uninstalled_deps.add(pkg_id)

    def flag_installed(self, installed: List[str]) -> None:
        """
        Ensure the dependency is not considered to still be uninstalled.

        Args:
            installed: the identifiers of packages that have been installed so far
        """
        now_installed = self.uninstalled_deps & set(installed)
        for pkg_id in now_installed:
            self.uninstalled_deps.remove(pkg_id)
            tty.debug(
                f"{self.pkg_id}: Removed {pkg_id} from uninstalled deps list: "
                f"{self.uninstalled_deps}",
                level=2,
            )

    def _setup_install_dir(self, pkg: "spack.package_base.PackageBase") -> None:
        """
        Create and ensure proper access controls for the install directory.
        Write a small metadata file with the current spack environment.

        Args:
            pkg: the package to be built and installed
        """
        # Move to a module level method.
        if not os.path.exists(pkg.spec.prefix):
            path = spack.util.path.debug_padded_filter(pkg.spec.prefix)
            tty.debug(f"Creating the installation directory {path}")
            spack.store.STORE.layout.create_install_directory(pkg.spec)
        else:
            # Set the proper group for the prefix
            group = prefs.get_package_group(pkg.spec)
            if group:
                fs.chgrp(pkg.spec.prefix, group)

            # Set the proper permissions.
            # This has to be done after group because changing groups blows
            # away the sticky group bit on the directory
            mode = os.stat(pkg.spec.prefix).st_mode
            perms = prefs.get_package_dir_permissions(pkg.spec)
            if mode != perms:
                os.chmod(pkg.spec.prefix, perms)

            # Ensure the metadata path exists as well
            fs.mkdirp(spack.store.STORE.layout.metadata_path(pkg.spec), mode=perms)

        # Always write host environment - we assume this can change
        spack.store.STORE.layout.write_host_environment(pkg.spec)

    @property
    def explicit(self) -> bool:
        return self.pkg.spec.dag_hash() in self.request.install_args.get("explicit", [])

    @property
    def is_build_request(self) -> bool:
        """The package was requested directly"""
        return self.pkg == self.request.pkg

    @property
    def use_cache(self) -> bool:
        _use_cache = True
        if self.is_build_request:
            return self.request.install_args.get("package_use_cache", _use_cache)
        else:
            return self.request.install_args.get("dependencies_use_cache", _use_cache)

    @property
    def cache_only(self) -> bool:
        _cache_only = False
        if self.is_build_request:
            return self.request.install_args.get("package_cache_only", _cache_only)
        else:
            return self.request.install_args.get("dependencies_cache_only", _cache_only)

    @property
    def key(self) -> Tuple[int, int]:
        """The key is the tuple (# uninstalled dependencies, sequence)."""
        return (self.priority, self.sequence)

    def next_attempt(self, installed) -> "Task":
        """Create a new, updated task for the next installation attempt."""
        task = copy.copy(self)
        task._update()
        task.start = self.start or time.time()
        task.flag_installed(installed)
        return task

    @property
    def priority(self):
        """The priority is based on the remaining uninstalled dependencies."""
        return len(self.uninstalled_deps)


class BuildTask(Task):
    """Class for representing a build task for a package."""

    def execute(self, install_status):
        """
        Perform the installation of the requested spec and/or dependency
        represented by the build task.
        """
        install_args = self.request.install_args
        tests = install_args.get("tests")
        unsigned = install_args.get("unsigned")

        pkg, pkg_id = self.pkg, self.pkg_id

        tty.msg(install_msg(pkg_id, self.pid, install_status))
        self.start = self.start or time.time()
        self.status = BuildStatus.INSTALLING

        # Use the binary cache if requested
        if self.use_cache:
            if _install_from_cache(pkg, self.explicit, unsigned):
                return ExecuteResult.SUCCESS
            elif self.cache_only:
                raise spack.error.InstallError(
                    "No binary found when cache-only was specified", pkg=pkg
                )
            else:
                tty.msg(f"No binary for {pkg_id} found: installing from source")

        pkg.run_tests = tests is True or tests and pkg.name in tests

        # hook that allows tests to inspect the Package before installation
        # see unit_test_check() docs.
        if not pkg.unit_test_check():
            return ExecuteResult.FAILED

        try:
            # Create stage object now and let it be serialized for the child process. That
            # way monkeypatch in tests works correctly.
            pkg.stage

            self._setup_install_dir(pkg)

            # Create a child process to do the actual installation.
            # Preserve verbosity settings across installs.
            spack.package_base.PackageBase._verbose = spack.build_environment.start_build_process(
                pkg, build_process, install_args
            )

            # Note: PARENT of the build process adds the new package to
            # the database, so that we don't need to re-read from file.
            spack.store.STORE.db.add(pkg.spec, explicit=self.explicit)
        except spack.error.StopPhase as e:
            # A StopPhase exception means that do_install was asked to
            # stop early from clients, and is not an error at this point
            pid = f"{self.pid}: " if tty.show_pid() else ""
            tty.debug(f"{pid}{str(e)}")
            tty.debug(f"Package stage directory: {pkg.stage.source_path}")
        return ExecuteResult.SUCCESS


class RewireTask(Task):
    """Class for representing a rewire task for a package."""

    def execute(self, install_status):
        """Execute rewire task

        Rewire tasks are executed by either rewiring self.package.spec.build_spec that is already
        installed or downloading and rewiring a binary for the it.

        If not available installed or as binary, return ExecuteResult.MISSING_BUILD_SPEC.
        This will prompt the Installer to requeue the task with a dependency on the BuildTask
        to install self.pkg.spec.build_spec
        """
        oldstatus = self.status
        self.status = BuildStatus.INSTALLING
        tty.msg(install_msg(self.pkg_id, self.pid, install_status))
        self.start = self.start or time.time()
        if not self.pkg.spec.build_spec.installed:
            try:
                install_args = self.request.install_args
                unsigned = install_args.get("unsigned")
                _process_binary_cache_tarball(self.pkg, explicit=self.explicit, unsigned=unsigned)
                _print_installed_pkg(self.pkg.prefix)
                return ExecuteResult.SUCCESS
            except BaseException as e:
                tty.error(f"Failed to rewire {self.pkg.spec} from binary. {e}")
                self.status = oldstatus
                return ExecuteResult.MISSING_BUILD_SPEC
        spack.rewiring.rewire_node(self.pkg.spec, self.explicit)
        _print_installed_pkg(self.pkg.prefix)
        return ExecuteResult.SUCCESS


class PackageInstaller:
    """
    Class for managing the install process for a Spack instance based on a bottom-up DAG approach.

    This installer can coordinate concurrent batch and interactive, local and distributed (on a
    shared file system) builds for the same Spack instance.
    """

    def __init__(
        self,
        packages: List["spack.package_base.PackageBase"],
        *,
        cache_only: bool = False,
        dependencies_cache_only: bool = False,
        dependencies_use_cache: bool = True,
        dirty: bool = False,
        explicit: Union[Set[str], bool] = False,
        overwrite: Optional[Union[List[str], Set[str]]] = None,
        fail_fast: bool = False,
        fake: bool = False,
        include_build_deps: bool = False,
        install_deps: bool = True,
        install_package: bool = True,
        install_source: bool = False,
        keep_prefix: bool = False,
        keep_stage: bool = False,
        package_cache_only: bool = False,
        package_use_cache: bool = True,
        restage: bool = False,
        skip_patch: bool = False,
        stop_at: Optional[str] = None,
        stop_before: Optional[str] = None,
        tests: Union[bool, List[str], Set[str]] = False,
        unsigned: Optional[bool] = None,
        use_cache: bool = False,
        verbose: bool = False,
    ) -> None:
        """
        Arguments:
            explicit: Set of package hashes to be marked as installed explicitly in the db. If
                True, the specs from ``packages`` are marked explicit, while their dependencies are
                not.
            fail_fast: Fail if any dependency fails to install; otherwise, the default is to
                install as many dependencies as possible (i.e., best effort installation).
            fake: Don't really build; install fake stub files instead.
            install_deps: Install dependencies before installing this package
            install_source: By default, source is not installed, but for debugging it might be
                useful to keep it around.
            keep_prefix: Keep install prefix on failure. By default, destroys it.
            keep_stage: By default, stage is destroyed only if there are no exceptions during
                build. Set to True to keep the stage even with exceptions.
            restage: Force spack to restage the package source.
            skip_patch: Skip patch stage of build if True.
            stop_before: stop execution before this installation phase (or None)
            stop_at: last installation phase to be executed (or None)
            tests: False to run no tests, True to test all packages, or a list of package names to
                run tests for some
            use_cache: Install from binary package, if available.
            verbose: Display verbose build output (by default, suppresses it)
        """
        if isinstance(explicit, bool):
            explicit = {pkg.spec.dag_hash() for pkg in packages} if explicit else set()

        install_args = {
            "cache_only": cache_only,
            "dependencies_cache_only": dependencies_cache_only,
            "dependencies_use_cache": dependencies_use_cache,
            "dirty": dirty,
            "explicit": explicit,
            "fail_fast": fail_fast,
            "fake": fake,
            "include_build_deps": include_build_deps,
            "install_deps": install_deps,
            "install_package": install_package,
            "install_source": install_source,
            "keep_prefix": keep_prefix,
            "keep_stage": keep_stage,
            "overwrite": overwrite or [],
            "package_cache_only": package_cache_only,
            "package_use_cache": package_use_cache,
            "restage": restage,
            "skip_patch": skip_patch,
            "stop_at": stop_at,
            "stop_before": stop_before,
            "tests": tests,
            "unsigned": unsigned,
            "use_cache": use_cache,
            "verbose": verbose,
        }

        # List of build requests
        self.build_requests = [BuildRequest(pkg, install_args) for pkg in packages]

        # Priority queue of tasks
        self.build_pq: List[Tuple[Tuple[int, int], Task]] = []

        # Mapping of unique package ids to task
        self.build_tasks: Dict[str, Task] = {}

        # Cache of package locks for failed packages, keyed on package's ids
        self.failed: Dict[str, Optional[lk.Lock]] = {}

        # Cache the PID for distributed build messaging
        self.pid: int = os.getpid()

        # Cache of installed packages' unique ids
        self.installed: Set[str] = set()

        # Data store layout
        self.layout = spack.store.STORE.layout

        # Locks on specs being built, keyed on the package's unique id
        self.locks: Dict[str, Tuple[str, Optional[lk.Lock]]] = {}

        # Cache fail_fast option to ensure if one build request asks to fail
        # fast then that option applies to all build requests.
        self.fail_fast = False

        # Initializing all_dependencies to empty. This will be set later in _init_queue.
        self.all_dependencies: Dict[str, Set[str]] = {}

    def __repr__(self) -> str:
        """Returns a formal representation of the package installer."""
        rep = f"{self.__class__.__name__}("
        for attr, value in self.__dict__.items():
            rep += f"{attr}={value.__repr__()}, "
        return f"{rep.strip(', ')})"

    def __str__(self) -> str:
        """Returns a printable version of the package installer."""
        requests = f"#requests={len(self.build_requests)}"
        tasks = f"#tasks={len(self.build_tasks)}"
        failed = f"failed ({len(self.failed)}) = {self.failed}"
        installed = f"installed ({len(self.installed)}) = {self.installed}"
        return f"{self.pid}: {requests}; {tasks}; {installed}; {failed}"

    def _add_init_task(
        self,
        pkg: "spack.package_base.PackageBase",
        request: BuildRequest,
        all_deps: Dict[str, Set[str]],
    ) -> None:
        """
        Creates and queues the initial task for the package.

        Args:
            pkg: the package to be built and installed
            request: the associated install request
            all_deps: dictionary of all dependencies and associated dependents
        """
        cls = RewireTask if pkg.spec.spliced else BuildTask
        task = cls(pkg, request=request, status=BuildStatus.QUEUED, installed=self.installed)
        for dep_id in task.dependencies:
            all_deps[dep_id].add(package_id(pkg.spec))

        self._push_task(task)

    def _check_db(
        self, spec: "spack.spec.Spec"
    ) -> Tuple[Optional[spack.database.InstallRecord], bool]:
        """Determine if the spec is flagged as installed in the database

        Args:
            spec: spec whose database install status is being checked

        Return:
            Tuple of optional database record, and a boolean installed_in_db
                that's ``True`` iff the spec is considered installed
        """
        try:
            rec = spack.store.STORE.db.get_record(spec)
            installed_in_db = rec.installed if rec else False
        except KeyError:
            # KeyError is raised if there is no matching spec in the database
            # (versus no matching specs that are installed).
            rec = None
            installed_in_db = False
        return rec, installed_in_db

    def _check_deps_status(self, request: BuildRequest) -> None:
        """Check the install status of the requested package

        Args:
            request: the associated install request
        """
        err = "Cannot proceed with {0}: {1}"
        for dep in request.traverse_dependencies():
            dep_pkg = dep.package
            dep_id = package_id(dep)

            # Check for failure since a prefix lock is not required
            if spack.store.STORE.failure_tracker.has_failed(dep):
                action = "'spack install' the dependency"
                msg = f"{dep_id} is marked as an install failure: {action}"
                raise spack.error.InstallError(err.format(request.pkg_id, msg), pkg=dep_pkg)

            # Attempt to get a read lock to ensure another process does not
            # uninstall the dependency while the requested spec is being
            # installed
            ltype, lock = self._ensure_locked("read", dep_pkg)
            if lock is None:
                msg = f"{dep_id} is write locked by another process"
                raise spack.error.InstallError(err.format(request.pkg_id, msg), pkg=request.pkg)

            # Flag external and upstream packages as being installed
            if dep_pkg.spec.external or dep_pkg.spec.installed_upstream:
                self._flag_installed(dep_pkg)
                continue

            # Check the database to see if the dependency has been installed
            # and flag as such if appropriate
            rec, installed_in_db = self._check_db(dep)
            if (
                rec
                and installed_in_db
                and (
                    dep.dag_hash() not in request.overwrite
                    or rec.installation_time > request.overwrite_time
                )
            ):
                tty.debug(f"Flagging {dep_id} as installed per the database")
                self._flag_installed(dep_pkg)
            else:
                lock.release_read()

    def _prepare_for_install(self, task: Task) -> None:
        """
        Check the database and leftover installation directories/files and
        prepare for a new install attempt for an uninstalled package.
        Preparation includes cleaning up installation and stage directories
        and ensuring the database is up-to-date.

        Args:
            task: the task whose associated package is
                being checked
        """
        install_args = task.request.install_args
        keep_prefix = install_args.get("keep_prefix")

        # Make sure the package is ready to be locally installed.
        self._ensure_install_ready(task.pkg)

        # Skip file system operations if we've already gone through them for
        # this spec.
        if task.pkg_id in self.installed:
            # Already determined the spec has been installed
            return

        # Determine if the spec is flagged as installed in the database
        rec, installed_in_db = self._check_db(task.pkg.spec)

        if not installed_in_db:
            # Ensure there is no other installed spec with the same prefix dir
            if spack.store.STORE.db.is_occupied_install_prefix(task.pkg.spec.prefix):
                raise spack.error.InstallError(
                    f"Install prefix collision for {task.pkg_id}",
                    long_msg=f"Prefix directory {task.pkg.spec.prefix} already "
                    "used by another installed spec.",
                    pkg=task.pkg,
                )

            # Make sure the installation directory is in the desired state
            # for uninstalled specs.
            if os.path.isdir(task.pkg.spec.prefix):
                if not keep_prefix:
                    task.pkg.remove_prefix()
                else:
                    tty.debug(f"{task.pkg_id} is partially installed")

        if (
            rec
            and installed_in_db
            and (
                rec.spec.dag_hash() not in task.request.overwrite
                or rec.installation_time > task.request.overwrite_time
            )
        ):
            self._update_installed(task)

            # Only update the explicit entry once for the explicit package
            if task.explicit:
                spack.store.STORE.db.update_explicit(task.pkg.spec, True)

    def _cleanup_all_tasks(self) -> None:
        """Cleanup all tasks to include releasing their locks."""
        for pkg_id in self.locks:
            self._release_lock(pkg_id)

        for pkg_id in self.failed:
            self._cleanup_failed(pkg_id)

        ids = list(self.build_tasks)
        for pkg_id in ids:
            try:
                self._remove_task(pkg_id)
            except Exception:
                pass

    def _cleanup_failed(self, pkg_id: str) -> None:
        """
        Cleanup any failed markers for the package

        Args:
            pkg_id (str): identifier for the failed package
        """
        lock = self.failed.get(pkg_id, None)
        if lock is not None:
            err = "{0} exception when removing failure tracking for {1}: {2}"
            try:
                tty.verbose(f"Removing failure mark on {pkg_id}")
                lock.release_write()
            except Exception as exc:
                tty.warn(err.format(exc.__class__.__name__, pkg_id, str(exc)))

    def _cleanup_task(self, pkg: "spack.package_base.PackageBase") -> None:
        """
        Cleanup the task for the spec

        Args:
            pkg: the package being installed
        """
        self._remove_task(package_id(pkg.spec))

        # Ensure we have a read lock to prevent others from uninstalling the
        # spec during our installation.
        self._ensure_locked("read", pkg)

    def _ensure_install_ready(self, pkg: "spack.package_base.PackageBase") -> None:
        """
        Ensure the package is ready to install locally, which includes
        already locked.

        Args:
            pkg: the package being locally installed
        """
        pkg_id = package_id(pkg.spec)
        pre = f"{pkg_id} cannot be installed locally:"

        # External packages cannot be installed locally.
        if pkg.spec.external:
            raise ExternalPackageError(f"{pre} is external")

        # Upstream packages cannot be installed locally.
        if pkg.spec.installed_upstream:
            raise UpstreamPackageError(f"{pre} is upstream")

        # The package must have a prefix lock at this stage.
        if pkg_id not in self.locks:
            raise InstallLockError(f"{pre} not locked")

    def _ensure_locked(
        self, lock_type: str, pkg: "spack.package_base.PackageBase"
    ) -> Tuple[str, Optional[lk.Lock]]:
        """
        Add a prefix lock of the specified type for the package spec

        If the lock exists, then adjust accordingly.  That is, read locks
        will be upgraded to write locks if a write lock is requested and
        write locks will be downgraded to read locks if a read lock is
        requested.

        The lock timeout for write locks is deliberately near zero seconds in
        order to ensure the current process proceeds as quickly as possible to
        the next spec.

        Args:
            lock_type: 'read' for a read lock, 'write' for a write lock
            pkg: the package whose spec is being installed

        Return:
            (lock_type, lock) tuple where lock will be None if it could not be obtained
        """
        assert lock_type in [
            "read",
            "write",
        ], f'"{lock_type}" is not a supported package management lock type'

        pkg_id = package_id(pkg.spec)
        ltype, lock = self.locks.get(pkg_id, (lock_type, None))
        if lock and ltype == lock_type:
            return ltype, lock

        desc = f"{lock_type} lock"
        msg = "{0} a {1} on {2} with timeout {3}"
        err = "Failed to {0} a {1} for {2} due to {3}: {4}"

        if lock_type == "read":
            # Wait until the other process finishes if there are no more
            # tasks with priority 0 (i.e., with no uninstalled
            # dependencies).
            no_p0 = len(self.build_tasks) == 0 or not self._next_is_pri0()
            timeout = None if no_p0 else 3.0
        else:
            timeout = 1e-9  # Near 0 to iterate through install specs quickly

        try:
            if lock is None:
                tty.debug(msg.format("Acquiring", desc, pkg_id, pretty_seconds(timeout or 0)))
                op = "acquire"
                lock = spack.store.STORE.prefix_locker.lock(pkg.spec, timeout)
                if timeout != lock.default_timeout:
                    tty.warn(f"Expected prefix lock timeout {timeout}, not {lock.default_timeout}")
                if lock_type == "read":
                    lock.acquire_read()
                else:
                    lock.acquire_write()

            elif lock_type == "read":  # write -> read
                # Only get here if the current lock is a write lock, which
                # must be downgraded to be a read lock
                # Retain the original lock timeout, which is in the lock's
                # default_timeout setting.
                tty.debug(
                    msg.format(
                        "Downgrading to", desc, pkg_id, pretty_seconds(lock.default_timeout or 0)
                    )
                )
                op = "downgrade to"
                lock.downgrade_write_to_read()

            else:  # read -> write
                # Only get here if the current lock is a read lock, which
                # must be upgraded to be a write lock
                tty.debug(msg.format("Upgrading to", desc, pkg_id, pretty_seconds(timeout or 0)))
                op = "upgrade to"
                lock.upgrade_read_to_write(timeout)
            tty.debug(f"{pkg_id} is now {lock_type} locked")

        except (lk.LockDowngradeError, lk.LockTimeoutError) as exc:
            tty.debug(err.format(op, desc, pkg_id, exc.__class__.__name__, str(exc)))
            return (lock_type, None)

        except (Exception, KeyboardInterrupt, SystemExit) as exc:
            tty.error(err.format(op, desc, pkg_id, exc.__class__.__name__, str(exc)))
            self._cleanup_all_tasks()
            raise

        self.locks[pkg_id] = (lock_type, lock)
        return self.locks[pkg_id]

    def _requeue_with_build_spec_tasks(self, task):
        """Requeue the task and its missing build spec dependencies"""
        # Full install of the build_spec is necessary because it didn't already exist somewhere
        spec = task.pkg.spec
        for dep in spec.build_spec.traverse():
            dep_pkg = dep.package

            dep_id = package_id(dep)
            if dep_id not in self.build_tasks:
                self._add_init_task(dep_pkg, task.request, self.all_dependencies)

            # Clear any persistent failure markings _unless_ they are
            # associated with another process in this parallel build
            # of the spec.
            spack.store.STORE.failure_tracker.clear(dep, force=False)

        # Queue the build spec.
        build_pkg_id = package_id(spec.build_spec)
        build_spec_task = self.build_tasks[build_pkg_id]
        spec_pkg_id = package_id(spec)
        spec_task = task.next_attempt(self.installed)
        spec_task.status = BuildStatus.QUEUED
        # Convey a build spec as a dependency of a deployed spec.
        build_spec_task.add_dependent(spec_pkg_id)
        spec_task.add_dependency(build_pkg_id)
        self._push_task(spec_task)

    def _add_tasks(self, request: BuildRequest, all_deps):
        """Add tasks to the priority queue for the given build request.

        It also tracks all dependents associated with each dependency in
        order to ensure proper tracking of uninstalled dependencies.

        Args:
            request (BuildRequest): the associated install request
            all_deps (defaultdict(set)): dictionary of all dependencies and
                associated dependents
        """
        tty.debug(f"Initializing the build queue for {request.pkg.name}")

        # Ensure not attempting to perform an installation when user didn't
        # want to go that far for the requested package.
        try:
            _check_last_phase(request.pkg)
        except BadInstallPhase as err:
            tty.warn(f"Installation request refused: {str(err)}")
            return

        install_deps = request.install_args.get("install_deps")

        if install_deps:
            for dep in request.traverse_dependencies():
                dep_pkg = dep.package

                dep_id = package_id(dep)
                if dep_id not in self.build_tasks:
                    self._add_init_task(dep_pkg, request, all_deps=all_deps)

                # Clear any persistent failure markings _unless_ they are
                # associated with another process in this parallel build
                # of the spec.
                spack.store.STORE.failure_tracker.clear(dep, force=False)

        install_package = request.install_args.get("install_package")
        if install_package and request.pkg_id not in self.build_tasks:
            # Be sure to clear any previous failure
            spack.store.STORE.failure_tracker.clear(request.spec, force=True)

            # If not installing dependencies, then determine their
            # installation status before proceeding
            if not install_deps:
                self._check_deps_status(request)

            # Now add the package itself, if appropriate
            self._add_init_task(request.pkg, request, all_deps=all_deps)

        # Ensure if one request is to fail fast then all requests will.
        fail_fast = bool(request.install_args.get("fail_fast"))
        self.fail_fast = self.fail_fast or fail_fast

    def _install_task(self, task: Task, install_status: InstallStatus) -> None:
        """
        Perform the installation of the requested spec and/or dependency
        represented by the task.

        Args:
            task: the installation task for a package
            install_status: the installation status for the package"""
        rc = task.execute(install_status)
        if rc == ExecuteResult.MISSING_BUILD_SPEC:
            self._requeue_with_build_spec_tasks(task)
        else:  # if rc == ExecuteResult.SUCCESS or rc == ExecuteResult.FAILED
            self._update_installed(task)

    def _next_is_pri0(self) -> bool:
        """
        Determine if the next task has priority 0

        Return:
            True if it does, False otherwise
        """
        # Leverage the fact that the first entry in the queue is the next
        # one that will be processed
        task = self.build_pq[0][1]
        return task.priority == 0

    def _pop_task(self) -> Optional[Task]:
        """
        Remove and return the lowest priority task.

        Source: Variant of function at docs.python.org/2/library/heapq.html
        """
        while self.build_pq:
            task = heapq.heappop(self.build_pq)[1]
            if task.status != BuildStatus.REMOVED:
                del self.build_tasks[task.pkg_id]
                task.status = BuildStatus.DEQUEUED
                return task
        return None

    def _push_task(self, task: Task) -> None:
        """
        Push (or queue) the specified task for the package.

        Source: Customization of "add_task" function at
                docs.python.org/2/library/heapq.html

        Args:
            task: the installation task for a package
        """
        msg = "{0} a task for {1} with status '{2}'"
        skip = "Skipping requeue of task for {0}: {1}"

        # Ensure do not (re-)queue installed or failed packages whose status
        # may have been determined by a separate process.
        if task.pkg_id in self.installed:
            tty.debug(skip.format(task.pkg_id, "installed"))
            return

        if task.pkg_id in self.failed:
            tty.debug(skip.format(task.pkg_id, "failed"))
            return

        # Remove any associated task since its sequence will change
        self._remove_task(task.pkg_id)
        desc = (
            "Queueing" if task.attempts == 1 else f"Requeueing ({ordinal(task.attempts)} attempt)"
        )
        tty.debug(msg.format(desc, task.pkg_id, task.status))

        # Now add the new task to the queue with a new sequence number to
        # ensure it is the last entry popped with the same priority.  This
        # is necessary in case we are re-queueing a task whose priority
        # was decremented due to the installation of one of its dependencies.
        self.build_tasks[task.pkg_id] = task
        heapq.heappush(self.build_pq, (task.key, task))

    def _release_lock(self, pkg_id: str) -> None:
        """
        Release any lock on the package

        Args:
            pkg_id (str): identifier for the package whose lock is be released
        """
        if pkg_id in self.locks:
            err = "{0} exception when releasing {1} lock for {2}: {3}"
            msg = "Releasing {0} lock on {1}"
            ltype, lock = self.locks[pkg_id]
            if lock is not None:
                try:
                    tty.debug(msg.format(ltype, pkg_id))
                    if ltype == "read":
                        lock.release_read()
                    else:
                        lock.release_write()
                except Exception as exc:
                    tty.warn(err.format(exc.__class__.__name__, ltype, pkg_id, str(exc)))

    def _remove_task(self, pkg_id: str) -> Optional[Task]:
        """
        Mark the existing package task as being removed and return it.
        Raises KeyError if not found.

        Source: Variant of function at docs.python.org/2/library/heapq.html

        Args:
            pkg_id: identifier for the package to be removed
        """
        if pkg_id in self.build_tasks:
            tty.debug(f"Removing task for {pkg_id} from list")
            task = self.build_tasks.pop(pkg_id)
            task.status = BuildStatus.REMOVED
            return task
        else:
            return None

    def _requeue_task(self, task: Task, install_status: InstallStatus) -> None:
        """
        Requeues a task that appears to be in progress by another process.

        Args:
            task (Task): the installation task for a package
        """
        if task.status not in [BuildStatus.INSTALLED, BuildStatus.INSTALLING]:
            tty.debug(
                f"{install_msg(task.pkg_id, self.pid, install_status)} "
                "in progress by another process"
            )

        new_task = task.next_attempt(self.installed)
        new_task.status = BuildStatus.INSTALLING
        self._push_task(new_task)

    def _update_failed(
        self, task: Task, mark: bool = False, exc: Optional[BaseException] = None
    ) -> None:
        """
        Update the task and transitive dependents as failed; optionally mark
        externally as failed; and remove associated tasks.

        Args:
            task: the task for the failed package
            mark: ``True`` if the package and its dependencies are to
                be marked as "failed", otherwise, ``False``
            exc: optional exception if associated with the failure
        """
        pkg_id = task.pkg_id
        err = "" if exc is None else f": {str(exc)}"
        tty.debug(f"Flagging {pkg_id} as failed{err}")
        if mark:
            self.failed[pkg_id] = spack.store.STORE.failure_tracker.mark(task.pkg.spec)
        else:
            self.failed[pkg_id] = None
        task.status = BuildStatus.FAILED

        for dep_id in task.dependents:
            if dep_id in self.build_tasks:
                tty.warn(f"Skipping build of {dep_id} since {pkg_id} failed")
                # Ensure the dependent's uninstalled dependents are
                # up-to-date and their tasks removed.
                dep_task = self.build_tasks[dep_id]
                self._update_failed(dep_task, mark)
                self._remove_task(dep_id)
            else:
                tty.debug(f"No task for {dep_id} to skip since {pkg_id} failed")

    def _update_installed(self, task: Task) -> None:
        """
        Mark the task as installed and ensure dependent tasks are aware.

        Args:
            task: the task for the installed package
        """
        task.status = BuildStatus.INSTALLED
        self._flag_installed(task.pkg, task.dependents)

    def _flag_installed(
        self, pkg: "spack.package_base.PackageBase", dependent_ids: Optional[Set[str]] = None
    ) -> None:
        """
        Flag the package as installed and ensure known by all tasks of
        known dependents.

        Args:
            pkg: Package that has been installed locally, externally or upstream
            dependent_ids: set of the package's dependent ids, or None if the dependent ids are
                limited to those maintained in the package (dependency DAG)
        """
        pkg_id = package_id(pkg.spec)

        if pkg_id in self.installed:
            # Already determined the package has been installed
            return

        tty.debug(f"Flagging {pkg_id} as installed")

        self.installed.add(pkg_id)

        # Update affected dependents
        dependent_ids = dependent_ids or get_dependent_ids(pkg.spec)
        for dep_id in set(dependent_ids):
            tty.debug(f"Removing {pkg_id} from {dep_id}'s uninstalled dependencies.")
            if dep_id in self.build_tasks:
                # Ensure the dependent's uninstalled dependencies are
                # up-to-date.  This will require requeueing the task.
                dep_task = self.build_tasks[dep_id]
                self._push_task(dep_task.next_attempt(self.installed))
            else:
                tty.debug(f"{dep_id} has no task to update for {pkg_id}'s success")

    def _init_queue(self) -> None:
        """Initialize the build queue from the list of build requests."""
        all_dependencies: Dict[str, Set[str]] = defaultdict(set)

        tty.debug("Initializing the build queue from the build requests")
        for request in self.build_requests:
            self._add_tasks(request, all_dependencies)

        # Add any missing dependents to ensure proper uninstalled dependency
        # tracking when installing multiple specs
        tty.debug("Ensure all dependencies know all dependents across specs")
        for dep_id in all_dependencies:
            if dep_id in self.build_tasks:
                dependents = all_dependencies[dep_id]
                task = self.build_tasks[dep_id]
                for dependent_id in dependents.difference(task.dependents):
                    task.add_dependent(dependent_id)
        self.all_dependencies = all_dependencies

    def _install_action(self, task: Task) -> InstallAction:
        """
        Determine whether the installation should be overwritten (if it already
        exists) or skipped (if has been handled by another process).

        If the package has not been installed yet, this will indicate that the
        installation should proceed as normal (i.e. no need to transactionally
        preserve the old prefix).
        """
        # If we don't have to overwrite, do a normal install
        if task.pkg.spec.dag_hash() not in task.request.overwrite:
            return InstallAction.INSTALL

        # If it's not installed, do a normal install as well
        rec, installed = self._check_db(task.pkg.spec)
        if not installed:
            return InstallAction.INSTALL

        # Ensure install_tree projections have not changed.
        assert rec and task.pkg.prefix == rec.path

        # If another process has overwritten this, we shouldn't install at all
        if rec.installation_time >= task.request.overwrite_time:
            return InstallAction.NONE

        # If the install prefix is missing, warn about it, and proceed with
        # normal install.
        if not os.path.exists(task.pkg.prefix):
            tty.debug("Missing installation to overwrite")
            return InstallAction.INSTALL

        # Otherwise, do an actual overwrite install. We backup the original
        # install directory, put the old prefix
        # back on failure
        return InstallAction.OVERWRITE

    def install(self) -> None:
        """Install the requested package(s) and or associated dependencies."""

        self._init_queue()
        fail_fast_err = "Terminating after first install failure"
        single_requested_spec = len(self.build_requests) == 1
        failed_build_requests = []

        install_status = InstallStatus(len(self.build_pq))

        # Only enable the terminal status line when we're in a tty without debug info
        # enabled, so that the output does not get cluttered.
        term_status = TermStatusLine(
            enabled=sys.stdout.isatty() and tty.msg_enabled() and not tty.is_debug()
        )

        while self.build_pq:
            task = self._pop_task()
            if task is None:
                continue

            install_args = task.request.install_args
            keep_prefix = install_args.get("keep_prefix")

            pkg, pkg_id, spec = task.pkg, task.pkg_id, task.pkg.spec
            install_status.next_pkg(pkg)
            install_status.set_term_title(f"Processing {pkg.name}")
            tty.debug(f"Processing {pkg_id}: task={task}")
            # Ensure that the current spec has NO uninstalled dependencies,
            # which is assumed to be reflected directly in its priority.
            #
            # If the spec has uninstalled dependencies, then there must be
            # a bug in the code (e.g., priority queue or uninstalled
            # dependencies handling).  So terminate under the assumption that
            # all subsequent tasks will have non-zero priorities or may be
            # dependencies of this task.
            if task.priority != 0:
                term_status.clear()
                tty.error(
                    f"Detected uninstalled dependencies for {pkg_id}: " f"{task.uninstalled_deps}"
                )
                left = [dep_id for dep_id in task.uninstalled_deps if dep_id not in self.installed]
                if not left:
                    tty.warn(f"{pkg_id} does NOT actually have any uninstalled deps left")
                dep_str = "dependencies" if task.priority > 1 else "dependency"

                raise spack.error.InstallError(
                    f"Cannot proceed with {pkg_id}: {task.priority} uninstalled "
                    f"{dep_str}: {','.join(task.uninstalled_deps)}",
                    pkg=pkg,
                )

            # Skip the installation if the spec is not being installed locally
            # (i.e., if external or upstream) BUT flag it as installed since
            # some package likely depends on it.
            if _handle_external_and_upstream(pkg, task.explicit):
                term_status.clear()
                self._flag_installed(pkg, task.dependents)
                continue

            # Flag a failed spec.  Do not need an (install) prefix lock since
            # assume using a separate (failed) prefix lock file.
            if pkg_id in self.failed or spack.store.STORE.failure_tracker.has_failed(spec):
                term_status.clear()
                tty.warn(f"{pkg_id} failed to install")
                self._update_failed(task)

                if self.fail_fast:
                    raise spack.error.InstallError(fail_fast_err, pkg=pkg)

                continue

            # Attempt to get a write lock.  If we can't get the lock then
            # another process is likely (un)installing the spec or has
            # determined the spec has already been installed (though the
            # other process may be hung).
            install_status.set_term_title(f"Acquiring lock for {pkg.name}")
            term_status.add(pkg_id)
            ltype, lock = self._ensure_locked("write", pkg)
            if lock is None:
                # Attempt to get a read lock instead.  If this fails then
                # another process has a write lock so must be (un)installing
                # the spec (or that process is hung).
                ltype, lock = self._ensure_locked("read", pkg)
            # Requeue the spec if we cannot get at least a read lock so we
            # can check the status presumably established by another process
            # -- failed, installed, or uninstalled -- on the next pass.
            if lock is None:
                self._requeue_task(task, install_status)
                continue

            term_status.clear()

            # Take a timestamp with the overwrite argument to allow checking
            # whether another process has already overridden the package.
            if task.request.overwrite and task.explicit:
                task.request.overwrite_time = time.time()

            # Determine state of installation artifacts and adjust accordingly.
            install_status.set_term_title(f"Preparing {pkg.name}")
            self._prepare_for_install(task)

            # Flag an already installed package
            if pkg_id in self.installed:
                # Downgrade to a read lock to preclude other processes from
                # uninstalling the package until we're done installing its
                # dependents.
                ltype, lock = self._ensure_locked("read", pkg)
                if lock is not None:
                    self._update_installed(task)
                    path = spack.util.path.debug_padded_filter(pkg.prefix)
                    _print_installed_pkg(path)
                else:
                    # At this point we've failed to get a write or a read
                    # lock, which means another process has taken a write
                    # lock between our releasing the write and acquiring the
                    # read.
                    #
                    # Requeue the task so we can re-check the status
                    # established by the other process -- failed, installed,
                    # or uninstalled -- on the next pass.
                    self.installed.remove(pkg_id)
                    self._requeue_task(task, install_status)
                continue

            # Having a read lock on an uninstalled pkg may mean another
            # process completed an uninstall of the software between the
            # time we failed to acquire the write lock and the time we
            # took the read lock.
            #
            # Requeue the task so we can check the status presumably
            # established by the other process -- failed, installed, or
            # uninstalled -- on the next pass.
            if ltype == "read":
                lock.release_read()
                self._requeue_task(task, install_status)
                continue

            # Proceed with the installation since we have an exclusive write
            # lock on the package.
            install_status.set_term_title(f"Installing {pkg.name}")
            try:
                action = self._install_action(task)

                if action == InstallAction.INSTALL:
                    self._install_task(task, install_status)
                elif action == InstallAction.OVERWRITE:
                    # spack.store.STORE.db is not really a Database object, but a small
                    # wrapper -- silence mypy
                    OverwriteInstall(self, spack.store.STORE.db, task, install_status).install()  # type: ignore[arg-type] # noqa: E501

                # If we installed then we should keep the prefix
                stop_before_phase = getattr(pkg, "stop_before_phase", None)
                last_phase = getattr(pkg, "last_phase", None)
                keep_prefix = keep_prefix or (stop_before_phase is None and last_phase is None)

            except KeyboardInterrupt as exc:
                # The build has been terminated with a Ctrl-C so terminate
                # regardless of the number of remaining specs.
                tty.error(
                    f"Failed to install {pkg.name} due to " f"{exc.__class__.__name__}: {str(exc)}"
                )
                raise

            except binary_distribution.NoChecksumException as exc:
                if task.cache_only:
                    raise

                # Checking hash on downloaded binary failed.
                tty.error(
                    f"Failed to install {pkg.name} from binary cache due "
                    f"to {str(exc)}: Requeueing to install from source."
                )
                # this overrides a full method, which is ugly.
                task.use_cache = False  # type: ignore[misc]
                self._requeue_task(task, install_status)
                continue

            except (Exception, SystemExit) as exc:
                self._update_failed(task, True, exc)

                # Best effort installs suppress the exception and mark the
                # package as a failure.
                if not isinstance(exc, spack.error.SpackError) or not exc.printed:  # type: ignore[union-attr] # noqa: E501
                    exc.printed = True  # type: ignore[union-attr]
                    # SpackErrors can be printed by the build process or at
                    # lower levels -- skip printing if already printed.
                    # TODO: sort out this and SpackError.print_context()
                    tty.error(
                        f"Failed to install {pkg.name} due to "
                        f"{exc.__class__.__name__}: {str(exc)}"
                    )
                # Terminate if requested to do so on the first failure.
                if self.fail_fast:
                    raise spack.error.InstallError(
                        f"{fail_fast_err}: {str(exc)}", pkg=pkg
                    ) from exc

                # Terminate when a single build request has failed, or summarize errors later.
                if task.is_build_request:
                    if single_requested_spec:
                        raise
                    failed_build_requests.append((pkg, pkg_id, str(exc)))

            finally:
                # Remove the install prefix if anything went wrong during
                # install.
                if not keep_prefix and not action == InstallAction.OVERWRITE:
                    pkg.remove_prefix()

            # Perform basic task cleanup for the installed spec to
            # include downgrading the write to a read lock
            if pkg.spec.installed:
                self._cleanup_task(pkg)

        # Cleanup, which includes releasing all of the read locks
        self._cleanup_all_tasks()

        # Ensure we properly report if one or more explicit specs failed
        # or were not installed when should have been.
        missing = [
            (request.pkg, request.pkg_id)
            for request in self.build_requests
            if request.install_args.get("install_package") and request.pkg_id not in self.installed
        ]

        if failed_build_requests or missing:
            for _, pkg_id, err in failed_build_requests:
                tty.error(f"{pkg_id}: {err}")

            for _, pkg_id in missing:
                tty.error(f"{pkg_id}: Package was not installed")

            if len(failed_build_requests) > 0:
                pkg = failed_build_requests[0][0]
                ids = [pkg_id for _, pkg_id, _ in failed_build_requests]
                tty.debug(
                    "Associating installation failure with first failed "
                    f"explicit package ({ids[0]}) from {', '.join(ids)}"
                )

            elif len(missing) > 0:
                pkg = missing[0][0]
                ids = [pkg_id for _, pkg_id in missing]
                tty.debug(
                    "Associating installation failure with first "
                    f"missing package ({ids[0]}) from {', '.join(ids)}"
                )

            raise spack.error.InstallError(
                "Installation request failed.  Refer to reported errors for failing package(s).",
                pkg=pkg,
            )


class BuildProcessInstaller:
    """This class implements the part installation that happens in the child process."""

    def __init__(self, pkg: "spack.package_base.PackageBase", install_args: dict):
        """Create a new BuildProcessInstaller.

        It is assumed that the lifecycle of this object is the same as the child
        process in the build.

        Arguments:
            pkg: the package being installed.
            install_args: arguments to the installer from parent process.

        """
        self.pkg = pkg

        # whether to do a fake install
        self.fake = install_args.get("fake", False)

        # whether to install source code with the packag
        self.install_source = install_args.get("install_source", False)

        is_develop = pkg.spec.is_develop
        # whether to keep the build stage after installation
        # Note: user commands do not have an explicit choice to disable
        # keeping stages (i.e., we have a --keep-stage option, but not
        # a --destroy-stage option), so we can override a default choice
        # to destroy
        self.keep_stage = is_develop or install_args.get("keep_stage", False)
        # whether to restage
        self.restage = (not is_develop) and install_args.get("restage", False)

        # whether to skip the patch phase
        self.skip_patch = install_args.get("skip_patch", False)

        # whether to enable echoing of build output initially or not
        self.verbose = bool(install_args.get("verbose", False))

        # whether installation was explicitly requested by the user
        self.explicit = pkg.spec.dag_hash() in install_args.get("explicit", [])

        # env before starting installation
        self.unmodified_env = install_args.get("unmodified_env", {})

        # env modifications by Spack
        self.env_mods = install_args.get("env_modifications", EnvironmentModifications())

        # timer for build phases
        self.timer = timer.Timer()

        # If we are using a padded path, filter the output to compress padded paths
        # The real log still has full-length paths.
        padding = spack.config.get("config:install_tree:padded_length", None)
        self.filter_fn = spack.util.path.padding_filter if padding else None

        # info/debug information
        self.pre = _log_prefix(pkg.name)
        self.pkg_id = package_id(pkg.spec)

    def run(self) -> bool:
        """Main entry point from ``build_process`` to kick off install in child."""

        stage = self.pkg.stage
        stage.keep = self.keep_stage

        if self.restage:
            stage.destroy()

        with stage:
            self.timer.start("stage")

            if not self.fake:
                if not self.skip_patch:
                    self.pkg.do_patch()
                else:
                    self.pkg.do_stage()

            self.timer.stop("stage")

            tty.debug(
                f"{self.pre} Building {self.pkg_id} [{self.pkg.build_system_class}]"  # type: ignore[attr-defined] # noqa: E501
            )

            # get verbosity from install parameter or saved value
            self.echo = self.verbose
            if spack.package_base.PackageBase._verbose is not None:
                self.echo = spack.package_base.PackageBase._verbose

            # Run the pre-install hook in the child process after
            # the directory is created.
            spack.hooks.pre_install(self.pkg.spec)
            if self.fake:
                _do_fake_install(self.pkg)
            else:
                if self.install_source:
                    self._install_source()

                self._real_install()

            # Run post install hooks before build stage is removed.
            self.timer.start("post-install")
            spack.hooks.post_install(self.pkg.spec, self.explicit)
            self.timer.stop("post-install")

            # Stop the timer and save results
            self.timer.stop()
            _write_timer_json(self.pkg, self.timer, False)

        print_install_test_log(self.pkg)
        _print_timer(pre=self.pre, pkg_id=self.pkg_id, timer=self.timer)
        _print_installed_pkg(self.pkg.prefix)

        # preserve verbosity across runs
        return self.echo

    def _install_source(self) -> None:
        """Install source code from stage into share/pkg/src if necessary."""
        pkg = self.pkg
        if not os.path.isdir(pkg.stage.source_path):
            return

        src_target = os.path.join(pkg.spec.prefix, "share", pkg.name, "src")
        tty.debug(f"{self.pre} Copying source to {src_target}")

        fs.install_tree(pkg.stage.source_path, src_target)

    def _real_install(self) -> None:
        import spack.builder

        pkg = self.pkg

        # Do the real install in the source directory.
        with fs.working_dir(pkg.stage.source_path):
            # Save the build environment in a file before building.
            dump_environment(pkg.env_path)

            # Save just the changes to the environment.  This file can be
            # safely installed, since it does not contain secret variables.
            with open(pkg.env_mods_path, "w") as env_mods_file:
                mods = self.env_mods.shell_modifications(explicit=True, env=self.unmodified_env)
                env_mods_file.write(mods)

            for attr in ("configure_args", "cmake_args"):
                try:
                    configure_args = getattr(pkg, attr)()
                    configure_args = " ".join(configure_args)

                    with open(pkg.configure_args_path, "w") as args_file:
                        args_file.write(configure_args)

                    break
                except Exception:
                    pass

            # cache debug settings
            debug_level = tty.debug_level()

            # Spawn a daemon that reads from a pipe and redirects
            # everything to log_path, and provide the phase for logging
            builder = spack.builder.create(pkg)
            for i, phase_fn in enumerate(builder):
                # Keep a log file for each phase
                log_dir = os.path.dirname(pkg.log_path)
                log_file = "spack-build-%02d-%s-out.txt" % (i + 1, phase_fn.name.lower())
                log_file = os.path.join(log_dir, log_file)

                try:
                    # DEBUGGING TIP - to debug this section, insert an IPython
                    # embed here, and run the sections below without log capture
                    log_contextmanager = log_output(
                        log_file,
                        self.echo,
                        True,
                        env=self.unmodified_env,
                        filter_fn=self.filter_fn,
                    )

                    with log_contextmanager as logger:
                        # Redirect stdout and stderr to daemon pipe
                        with logger.force_echo():
                            inner_debug_level = tty.debug_level()
                            tty.set_debug(debug_level)
                            tty.msg(f"{self.pre} Executing phase: '{phase_fn.name}'")
                            tty.set_debug(inner_debug_level)

                        # Catch any errors to report to logging
                        self.timer.start(phase_fn.name)
                        phase_fn.execute()
                        self.timer.stop(phase_fn.name)

                except BaseException:
                    combine_phase_logs(pkg.phase_log_files, pkg.log_path)
                    raise

                # We assume loggers share echo True/False
                self.echo = logger.echo

        # After log, we can get all output/error files from the package stage
        combine_phase_logs(pkg.phase_log_files, pkg.log_path)
        log(pkg)


def build_process(pkg: "spack.package_base.PackageBase", install_args: dict) -> bool:
    """Perform the installation/build of the package.

    This runs in a separate child process, and has its own process and
    python module space set up by build_environment.start_build_process().

    This essentially wraps an instance of ``BuildProcessInstaller`` so that we can
    more easily create one in a subprocess.

    This function's return value is returned to the parent process.

    Arguments:
        pkg: the package being installed.
        install_args: arguments to installer from parent process.

    """
    installer = BuildProcessInstaller(pkg, install_args)

    # don't print long padded paths in executable debug output.
    with spack.util.path.filter_padding():
        return installer.run()


def deprecate(spec: "spack.spec.Spec", deprecator: "spack.spec.Spec", link_fn) -> None:
    """Deprecate this package in favor of deprecator spec"""
    # Here we assume we don't deprecate across different stores, and that same hash
    # means same binary artifacts
    if spec.dag_hash() == deprecator.dag_hash():
        return

    # We can't really have control over external specs, and cannot link anything in their place
    if spec.external:
        return

    # Install deprecator if it isn't installed already
    if not spack.store.STORE.db.query(deprecator):
        PackageInstaller([deprecator.package], explicit=True).install()

    old_deprecator = spack.store.STORE.db.deprecator(spec)
    if old_deprecator:
        # Find this spec file from its old deprecation
        specfile = spack.store.STORE.layout.deprecated_file_path(spec, old_deprecator)
    else:
        specfile = spack.store.STORE.layout.spec_file_path(spec)

    # copy spec metadata to "deprecated" dir of deprecator
    depr_specfile = spack.store.STORE.layout.deprecated_file_path(spec, deprecator)
    fs.mkdirp(os.path.dirname(depr_specfile))
    shutil.copy2(specfile, depr_specfile)

    # Any specs deprecated in favor of this spec are re-deprecated in favor of its new deprecator
    for deprecated in spack.store.STORE.db.specs_deprecated_by(spec):
        deprecate(deprecated, deprecator, link_fn)

    # Now that we've handled metadata, uninstall and replace with link
    spack.package_base.PackageBase.uninstall_by_spec(spec, force=True, deprecator=deprecator)
    link_fn(deprecator.prefix, spec.prefix)


class OverwriteInstall:
    def __init__(
        self,
        installer: PackageInstaller,
        database: spack.database.Database,
        task: Task,
        install_status: InstallStatus,
    ):
        self.installer = installer
        self.database = database
        self.task = task
        self.install_status = install_status

    def install(self):
        """
        Try to run the install task overwriting the package prefix.
        If this fails, try to recover the original install prefix. If that fails
        too, mark the spec as uninstalled. This function always the original
        install error if installation fails.
        """
        try:
            with fs.replace_directory_transaction(self.task.pkg.prefix):
                self.installer._install_task(self.task, self.install_status)
        except fs.CouldNotRestoreDirectoryBackup as e:
            self.database.remove(self.task.pkg.spec)
            tty.error(
                f"Recovery of install dir of {self.task.pkg.name} failed due to "
                f"{e.outer_exception.__class__.__name__}: {str(e.outer_exception)}. "
                "The spec is now uninstalled."
            )

            # Unwrap the actual installation exception.
            raise e.inner_exception


class BadInstallPhase(spack.error.InstallError):
    """Raised for an install phase option is not allowed for a package."""

    def __init__(self, pkg_name, phase):
        super().__init__(f"'{phase}' is not a valid phase for package {pkg_name}")


class ExternalPackageError(spack.error.InstallError):
    """Raised by install() when a package is only for external use."""


class InstallLockError(spack.error.InstallError):
    """Raised during install when something goes wrong with package locking."""


class UpstreamPackageError(spack.error.InstallError):
    """Raised during install when something goes wrong with an upstream
    package."""
