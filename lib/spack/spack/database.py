# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Spack's installation tracking database.

The database serves two purposes:

  1. It implements a cache on top of a potentially very large Spack
     directory hierarchy, speeding up many operations that would
     otherwise require filesystem access.

  2. It will allow us to track external installations as well as lost
     packages and their dependencies.

Prior to the implementation of this store, a directory layout served
as the authoritative database of packages in Spack.  This module
provides a cache and a sanity checking mechanism for what is in the
filesystem.
"""
import contextlib
import datetime
import os
import pathlib
import socket
import sys
import time
from json import JSONDecoder
from typing import (
    Any,
    Callable,
    Container,
    Dict,
    Generator,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)

try:
    import uuid

    _use_uuid = True
except ImportError:
    _use_uuid = False
    pass

import llnl.util.filesystem as fs
import llnl.util.lang
import llnl.util.tty as tty

import spack.deptypes as dt
import spack.hash_types as ht
import spack.spec
import spack.traverse as tr
import spack.util.lock as lk
import spack.util.spack_json as sjson
import spack.version as vn
from spack.directory_layout import (
    DirectoryLayout,
    DirectoryLayoutError,
    InconsistentInstallDirectoryError,
)
from spack.error import SpackError
from spack.util.crypto import bit_length

# TODO: Provide an API automatically retyring a build after detecting and
# TODO: clearing a failure.

#: DB goes in this directory underneath the root
_DB_DIRNAME = ".spack-db"

#: DB version.  This is stuck in the DB file to track changes in format.
#: Increment by one when the database format changes.
#: Versions before 5 were not integers.
_DB_VERSION = vn.Version("7")

#: For any version combinations here, skip reindex when upgrading.
#: Reindexing can take considerable time and is not always necessary.
_SKIP_REINDEX = [
    # reindexing takes a significant amount of time, and there's
    # no reason to do it from DB version 0.9.3 to version 5. The
    # only difference is that v5 can contain "deprecated_for"
    # fields.  So, skip the reindex for this transition. The new
    # version is saved to disk the first time the DB is written.
    (vn.Version("0.9.3"), vn.Version("5")),
    (vn.Version("5"), vn.Version("6")),
    (vn.Version("6"), vn.Version("7")),
]

#: Default timeout for spack database locks in seconds or None (no timeout).
#: A balance needs to be struck between quick turnaround for parallel installs
#: (to avoid excess delays) and waiting long enough when the system is busy
#: (to ensure the database is updated).
_DEFAULT_DB_LOCK_TIMEOUT = 120

#: Default timeout for spack package locks in seconds or None (no timeout).
#: A balance needs to be struck between quick turnaround for parallel installs
#: (to avoid excess delays when performing a parallel installation) and waiting
#: long enough for the next possible spec to install (to avoid excessive
#: checking of the last high priority package) or holding on to a lock (to
#: ensure a failed install is properly tracked).
_DEFAULT_PKG_LOCK_TIMEOUT = None

#: Types of dependencies tracked by the database
#: We store by DAG hash, so we track the dependencies that the DAG hash includes.
_TRACKED_DEPENDENCIES = ht.dag_hash.depflag

#: Default list of fields written for each install record
DEFAULT_INSTALL_RECORD_FIELDS = (
    "spec",
    "ref_count",
    "path",
    "installed",
    "explicit",
    "installation_time",
    "deprecated_for",
)


@llnl.util.lang.memoized
def _getfqdn():
    """Memoized version of `getfqdn()`.

    If we call `getfqdn()` too many times, DNS can be very slow. We only need to call it
    one time per process, so we cache it here.

    """
    return socket.getfqdn()


def reader(version: vn.StandardVersion) -> Type["spack.spec.SpecfileReaderBase"]:
    reader_cls = {
        vn.Version("5"): spack.spec.SpecfileV1,
        vn.Version("6"): spack.spec.SpecfileV3,
        vn.Version("7"): spack.spec.SpecfileV4,
    }
    return reader_cls[version]


def _now() -> float:
    """Returns the time since the epoch"""
    return time.time()


def _autospec(function):
    """Decorator that automatically converts the argument of a single-arg
    function to a Spec."""

    def converter(self, spec_like, *args, **kwargs):
        if not isinstance(spec_like, spack.spec.Spec):
            spec_like = spack.spec.Spec(spec_like)
        return function(self, spec_like, *args, **kwargs)

    return converter


class InstallStatus(str):
    pass


class InstallStatuses:
    INSTALLED = InstallStatus("installed")
    DEPRECATED = InstallStatus("deprecated")
    MISSING = InstallStatus("missing")

    @classmethod
    def canonicalize(cls, query_arg):
        if query_arg is True:
            return [cls.INSTALLED]
        if query_arg is False:
            return [cls.MISSING]
        if query_arg is any:
            return [cls.INSTALLED, cls.DEPRECATED, cls.MISSING]
        if isinstance(query_arg, InstallStatus):
            return [query_arg]
        try:
            statuses = list(query_arg)
            if all(isinstance(x, InstallStatus) for x in statuses):
                return statuses
        except TypeError:
            pass

        raise TypeError(
            "installation query must be `any`, boolean, "
            "InstallStatus, or iterable of InstallStatus"
        )


class InstallRecord:
    """A record represents one installation in the DB.

    The record keeps track of the spec for the installation, its
    install path, AND whether or not it is installed.  We need the
    installed flag in case a user either:

        a) blew away a directory, or
        b) used spack uninstall -f to get rid of it

    If, in either case, the package was removed but others still
    depend on it, we still need to track its spec, so we don't
    actually remove from the database until a spec has no installed
    dependents left.

    Args:
        spec: spec tracked by the install record
        path: path where the spec has been installed
        installed: whether or not the spec is currently installed
        ref_count (int): number of specs that depend on this one
        explicit (bool or None): whether or not this spec was explicitly
            installed, or pulled-in as a dependency of something else
        installation_time (datetime.datetime or None): time of the installation
    """

    def __init__(
        self,
        spec: "spack.spec.Spec",
        path: Optional[str],
        installed: bool,
        ref_count: int = 0,
        explicit: bool = False,
        installation_time: Optional[float] = None,
        deprecated_for: Optional[str] = None,
        in_buildcache: bool = False,
        origin=None,
    ):
        self.spec = spec
        self.path = str(path) if path else None
        self.installed = bool(installed)
        self.ref_count = ref_count
        self.explicit = explicit
        self.installation_time = installation_time or _now()
        self.deprecated_for = deprecated_for
        self.in_buildcache = in_buildcache
        self.origin = origin

    def install_type_matches(self, installed):
        installed = InstallStatuses.canonicalize(installed)
        if self.installed:
            return InstallStatuses.INSTALLED in installed
        elif self.deprecated_for:
            return InstallStatuses.DEPRECATED in installed
        else:
            return InstallStatuses.MISSING in installed

    def to_dict(self, include_fields=DEFAULT_INSTALL_RECORD_FIELDS):
        rec_dict = {}

        for field_name in include_fields:
            if field_name == "spec":
                rec_dict.update({"spec": self.spec.node_dict_with_hashes()})
            elif field_name == "deprecated_for" and self.deprecated_for:
                rec_dict.update({"deprecated_for": self.deprecated_for})
            else:
                rec_dict.update({field_name: getattr(self, field_name)})

        if self.origin:
            rec_dict["origin"] = self.origin

        return rec_dict

    @classmethod
    def from_dict(cls, spec, dictionary):
        d = dict(dictionary.items())
        d.pop("spec", None)

        # Old databases may have "None" for path for externals
        if "path" not in d or d["path"] == "None":
            d["path"] = None

        if "installed" not in d:
            d["installed"] = False

        return InstallRecord(spec, **d)


class ForbiddenLockError(SpackError):
    """Raised when an upstream DB attempts to acquire a lock"""


class ForbiddenLock:
    def __getattr__(self, name):
        raise ForbiddenLockError("Cannot access attribute '{0}' of lock".format(name))

    def __reduce__(self):
        return ForbiddenLock, tuple()


_QUERY_DOCSTRING = """

        Args:
            query_spec: queries iterate through specs in the database and
                return those that satisfy the supplied ``query_spec``. If
                query_spec is `any`, This will match all specs in the
                database.  If it is a spec, we'll evaluate
                ``spec.satisfies(query_spec)``

            known (bool or None): Specs that are "known" are those
                for which Spack can locate a ``package.py`` file -- i.e.,
                Spack "knows" how to install them.  Specs that are unknown may
                represent packages that existed in a previous version of
                Spack, but have since either changed their name or
                been removed

            installed (bool or InstallStatus or typing.Iterable or None):
                if ``True``, includes only installed
                specs in the search; if ``False`` only missing specs, and if
                ``any``, all specs in database. If an InstallStatus or iterable
                of InstallStatus, returns specs whose install status
                (installed, deprecated, or missing) matches (one of) the
                InstallStatus. (default: True)

            explicit (bool or None): A spec that was installed
                following a specific user request is marked as explicit. If
                instead it was pulled-in as a dependency of a user requested
                spec it's considered implicit.

            start_date (datetime.datetime or None): filters the query
                discarding specs that have been installed before ``start_date``.

            end_date (datetime.datetime or None): filters the query discarding
                specs that have been installed after ``end_date``.

            hashes (Container): list or set of hashes that we can use to
                restrict the search

            in_buildcache (bool or None): Specs that are marked in
                this database as part of an associated binary cache are
                ``in_buildcache``. All other specs are not. This field is used
                for querying mirror indices. Default is ``any``.

        Returns:
            list of specs that match the query

        """


class LockConfiguration(NamedTuple):
    """Data class to configure locks in Database objects

    Args:
        enable: whether to enable locks or not.
        database_timeout: timeout for the database lock
        package_timeout: timeout for the package lock
    """

    enable: bool
    database_timeout: Optional[int]
    package_timeout: Optional[int]


#: Configure a database to avoid using locks
NO_LOCK: LockConfiguration = LockConfiguration(
    enable=False, database_timeout=None, package_timeout=None
)


#: Configure the database to use locks without a timeout
NO_TIMEOUT: LockConfiguration = LockConfiguration(
    enable=True, database_timeout=None, package_timeout=None
)

#: Default configuration for database locks
DEFAULT_LOCK_CFG: LockConfiguration = LockConfiguration(
    enable=True,
    database_timeout=_DEFAULT_DB_LOCK_TIMEOUT,
    package_timeout=_DEFAULT_PKG_LOCK_TIMEOUT,
)


def lock_configuration(configuration):
    """Return a LockConfiguration from a spack.config.Configuration object."""
    return LockConfiguration(
        enable=configuration.get("config:locks", True),
        database_timeout=configuration.get("config:db_lock_timeout"),
        package_timeout=configuration.get("config:package_lock_timeout"),
    )


def prefix_lock_path(root_dir: Union[str, pathlib.Path]) -> pathlib.Path:
    """Returns the path of the prefix lock file, given the root directory.

    Args:
        root_dir: root directory containing the database directory
    """
    return pathlib.Path(root_dir) / _DB_DIRNAME / "prefix_lock"


def failures_lock_path(root_dir: Union[str, pathlib.Path]) -> pathlib.Path:
    """Returns the path of the failures lock file, given the root directory.

    Args:
        root_dir: root directory containing the database directory
    """
    return pathlib.Path(root_dir) / _DB_DIRNAME / "prefix_failures"


class SpecLocker:
    """Manages acquiring and releasing read or write locks on concrete specs."""

    def __init__(self, lock_path: Union[str, pathlib.Path], default_timeout: Optional[float]):
        self.lock_path = pathlib.Path(lock_path)
        self.default_timeout = default_timeout

        # Maps (spec.dag_hash(), spec.name) to the corresponding lock object
        self.locks: Dict[Tuple[str, str], lk.Lock] = {}

    def lock(self, spec: "spack.spec.Spec", timeout: Optional[float] = None) -> lk.Lock:
        """Returns a lock on a concrete spec.

        The lock is a byte range lock on the nth byte of a file.

        The lock file is ``self.lock_path``.

        n is the sys.maxsize-bit prefix of the DAG hash.  This makes likelihood of collision is
        very low AND it gives us readers-writer lock semantics with just a single lockfile, so
        no cleanup required.
        """
        assert spec.concrete, "cannot lock a non-concrete spec"
        timeout = timeout or self.default_timeout
        key = self._lock_key(spec)

        if key not in self.locks:
            self.locks[key] = self.raw_lock(spec, timeout=timeout)
        else:
            self.locks[key].default_timeout = timeout

        return self.locks[key]

    def raw_lock(self, spec: "spack.spec.Spec", timeout: Optional[float] = None) -> lk.Lock:
        """Returns a raw lock for a Spec, but doesn't keep track of it."""
        return lk.Lock(
            str(self.lock_path),
            start=spec.dag_hash_bit_prefix(bit_length(sys.maxsize)),
            length=1,
            default_timeout=timeout,
            desc=spec.name,
        )

    def has_lock(self, spec: "spack.spec.Spec") -> bool:
        """Returns True if the spec is already managed by this spec locker"""
        return self._lock_key(spec) in self.locks

    def _lock_key(self, spec: "spack.spec.Spec") -> Tuple[str, str]:
        return (spec.dag_hash(), spec.name)

    @contextlib.contextmanager
    def write_lock(self, spec: "spack.spec.Spec") -> Generator["SpecLocker", None, None]:
        lock = self.lock(spec)
        lock.acquire_write()

        try:
            yield self
        except lk.LockError:
            # This addresses the case where a nested lock attempt fails inside
            # of this context manager
            raise
        except (Exception, KeyboardInterrupt):
            lock.release_write()
            raise
        else:
            lock.release_write()

    def clear(self, spec: "spack.spec.Spec") -> Tuple[bool, Optional[lk.Lock]]:
        key = self._lock_key(spec)
        lock = self.locks.pop(key, None)
        return bool(lock), lock

    def clear_all(self, clear_fn: Optional[Callable[[lk.Lock], Any]] = None) -> None:
        if clear_fn is not None:
            for lock in self.locks.values():
                clear_fn(lock)
        self.locks.clear()


class FailureTracker:
    """Tracks installation failures.

    Prefix failure marking takes the form of a byte range lock on the nth
    byte of a file for coordinating between concurrent parallel build
    processes and a persistent file, named with the full hash and
    containing the spec, in a subdirectory of the database to enable
    persistence across overlapping but separate related build processes.

    The failure lock file lives alongside the install DB.

    ``n`` is the sys.maxsize-bit prefix of the associated DAG hash to make
    the likelihood of collision very low with no cleanup required.
    """

    def __init__(self, root_dir: Union[str, pathlib.Path], default_timeout: Optional[float]):
        #: Ensure a persistent location for dealing with parallel installation
        #: failures (e.g., across near-concurrent processes).
        self.dir = pathlib.Path(root_dir) / _DB_DIRNAME / "failures"
        self.dir.mkdir(parents=True, exist_ok=True)

        self.locker = SpecLocker(failures_lock_path(root_dir), default_timeout=default_timeout)

    def clear(self, spec: "spack.spec.Spec", force: bool = False) -> None:
        """Removes any persistent and cached failure tracking for the spec.

        see `mark()`.

        Args:
            spec: the spec whose failure indicators are being removed
            force: True if the failure information should be cleared when a failure lock
                exists for the file, or False if the failure should not be cleared (e.g.,
                it may be associated with a concurrent build)
        """
        locked = self.lock_taken(spec)
        if locked and not force:
            tty.msg(f"Retaining failure marking for {spec.name} due to lock")
            return

        if locked:
            tty.warn(f"Removing failure marking despite lock for {spec.name}")

        succeeded, lock = self.locker.clear(spec)
        if succeeded and lock is not None:
            lock.release_write()

        if self.persistent_mark(spec):
            path = self._path(spec)
            tty.debug(f"Removing failure marking for {spec.name}")
            try:
                path.unlink()
            except OSError as err:
                tty.warn(
                    f"Unable to remove failure marking for {spec.name} ({str(path)}): {str(err)}"
                )

    def clear_all(self) -> None:
        """Force remove install failure tracking files."""
        tty.debug("Releasing prefix failure locks")
        self.locker.clear_all(
            clear_fn=lambda x: x.release_write() if x.is_write_locked() else True
        )

        tty.debug("Removing prefix failure tracking files")
        try:
            for fail_mark in os.listdir(str(self.dir)):
                try:
                    (self.dir / fail_mark).unlink()
                except OSError as exc:
                    tty.warn(f"Unable to remove failure marking file {fail_mark}: {str(exc)}")
        except OSError as exc:
            tty.warn(f"Unable to remove failure marking files: {str(exc)}")

    def mark(self, spec: "spack.spec.Spec") -> lk.Lock:
        """Marks a spec as failing to install.

        Args:
            spec: spec that failed to install
        """
        # Dump the spec to the failure file for (manual) debugging purposes
        path = self._path(spec)
        path.write_text(spec.to_json())

        # Also ensure a failure lock is taken to prevent cleanup removal
        # of failure status information during a concurrent parallel build.
        if not self.locker.has_lock(spec):
            try:
                mark = self.locker.lock(spec)
                mark.acquire_write()
            except lk.LockTimeoutError:
                # Unlikely that another process failed to install at the same
                # time but log it anyway.
                tty.debug(f"PID {os.getpid()} failed to mark install failure for {spec.name}")
                tty.warn(f"Unable to mark {spec.name} as failed.")

        return self.locker.lock(spec)

    def has_failed(self, spec: "spack.spec.Spec") -> bool:
        """Return True if the spec is marked as failed."""
        # The failure was detected in this process.
        if self.locker.has_lock(spec):
            return True

        # The failure was detected by a concurrent process (e.g., an srun),
        # which is expected to be holding a write lock if that is the case.
        if self.lock_taken(spec):
            return True

        # Determine if the spec may have been marked as failed by a separate
        # spack build process running concurrently.
        return self.persistent_mark(spec)

    def lock_taken(self, spec: "spack.spec.Spec") -> bool:
        """Return True if another process has a failure lock on the spec."""
        check = self.locker.raw_lock(spec)
        return check.is_write_locked()

    def persistent_mark(self, spec: "spack.spec.Spec") -> bool:
        """Determine if the spec has a persistent failure marking."""
        return self._path(spec).exists()

    def _path(self, spec: "spack.spec.Spec") -> pathlib.Path:
        """Return the path to the spec's failure file, which may not exist."""
        assert spec.concrete, "concrete spec required for failure path"
        return self.dir / f"{spec.name}-{spec.dag_hash()}"


class Database:
    #: Fields written for each install record
    record_fields: Tuple[str, ...] = DEFAULT_INSTALL_RECORD_FIELDS

    def __init__(
        self,
        root: str,
        *,
        upstream_dbs: Optional[List["Database"]] = None,
        is_upstream: bool = False,
        lock_cfg: LockConfiguration = DEFAULT_LOCK_CFG,
        layout: Optional[DirectoryLayout] = None,
    ) -> None:
        """Database for Spack installations.

        A Database is a cache of Specs data from ``$prefix/spec.yaml`` files
        in Spack installation directories.

        Database files (data and lock files) are stored under ``root/.spack-db``, which is
        created if it does not exist.  This is the "database directory".

        The database will attempt to read an ``index.json`` file in the database directory.
        If that does not exist, it will create a database when needed by scanning the entire
        store root for ``spec.json`` files according to Spack's directory layout.

        Args:
            root: root directory where to create the database directory.
            upstream_dbs: upstream databases for this repository.
            is_upstream: whether this repository is an upstream.
            lock_cfg: configuration for the locks to be used by this repository.
                Relevant only if the repository is not an upstream.
        """
        self.root = root
        self.database_directory = os.path.join(self.root, _DB_DIRNAME)
        self.layout = layout

        # Set up layout of database files within the db dir
        self._index_path = os.path.join(self.database_directory, "index.json")
        self._verifier_path = os.path.join(self.database_directory, "index_verifier")
        self._lock_path = os.path.join(self.database_directory, "lock")

        # Create needed directories and files
        if not is_upstream and not os.path.exists(self.database_directory):
            fs.mkdirp(self.database_directory)

        self.is_upstream = is_upstream
        self.last_seen_verifier = ""
        # Failed write transactions (interrupted by exceptions) will alert
        # _write. When that happens, we set this flag to indicate that
        # future read/write transactions should re-read the DB. Normally it
        # would make more sense to resolve this at the end of the transaction
        # but typically a failed transaction will terminate the running
        # instance of Spack and we don't want to incur an extra read in that
        # case, so we defer the cleanup to when we begin the next transaction
        self._state_is_inconsistent = False

        # initialize rest of state.
        self.db_lock_timeout = lock_cfg.database_timeout
        tty.debug("DATABASE LOCK TIMEOUT: {0}s".format(str(self.db_lock_timeout)))

        self.lock: Union[ForbiddenLock, lk.Lock]
        if self.is_upstream:
            self.lock = ForbiddenLock()
        else:
            self.lock = lk.Lock(
                self._lock_path,
                default_timeout=self.db_lock_timeout,
                desc="database",
                enable=lock_cfg.enable,
            )
        self._data: Dict[str, InstallRecord] = {}

        # For every installed spec we keep track of its install prefix, so that
        # we can answer the simple query whether a given path is already taken
        # before installing a different spec.
        self._installed_prefixes: Set[str] = set()

        self.upstream_dbs = list(upstream_dbs) if upstream_dbs else []

        self._write_transaction_impl = lk.WriteTransaction
        self._read_transaction_impl = lk.ReadTransaction

    def write_transaction(self):
        """Get a write lock context manager for use in a `with` block."""
        return self._write_transaction_impl(self.lock, acquire=self._read, release=self._write)

    def read_transaction(self):
        """Get a read lock context manager for use in a `with` block."""
        return self._read_transaction_impl(self.lock, acquire=self._read)

    def _write_to_file(self, stream):
        """Write out the database in JSON format to the stream passed
        as argument.

        This function does not do any locking or transactions.
        """
        # map from per-spec hash code to installation record.
        installs = dict(
            (k, v.to_dict(include_fields=self.record_fields)) for k, v in self._data.items()
        )

        # database includes installation list and version.

        # NOTE: this DB version does not handle multiple installs of
        # the same spec well.  If there are 2 identical specs with
        # different paths, it can't differentiate.
        # TODO: fix this before we support multiple install locations.
        database = {
            "database": {
                # TODO: move this to a top-level _meta section if we ever
                # TODO: bump the DB version to 7
                "version": str(_DB_VERSION),
                # dictionary of installation records, keyed by DAG hash
                "installs": installs,
            }
        }

        try:
            sjson.dump(database, stream)
        except (TypeError, ValueError) as e:
            raise sjson.SpackJSONError("error writing JSON database:", str(e))

    def _read_spec_from_dict(self, spec_reader, hash_key, installs, hash=ht.dag_hash):
        """Recursively construct a spec from a hash in a YAML database.

        Does not do any locking.
        """
        spec_dict = installs[hash_key]["spec"]

        # Install records don't include hash with spec, so we add it in here
        # to ensure it is read properly.
        if "name" not in spec_dict.keys():
            # old format, can't update format here
            for name in spec_dict:
                spec_dict[name]["hash"] = hash_key
        else:
            # new format, already a singleton
            spec_dict[hash.name] = hash_key

        # Build spec from dict first.
        return spec_reader.from_node_dict(spec_dict)

    def db_for_spec_hash(self, hash_key):
        with self.read_transaction():
            if hash_key in self._data:
                return self

        for db in self.upstream_dbs:
            if hash_key in db._data:
                return db

    def query_by_spec_hash(
        self, hash_key: str, data: Optional[Dict[str, InstallRecord]] = None
    ) -> Tuple[bool, Optional[InstallRecord]]:
        """Get a spec for hash, and whether it's installed upstream.

        Return:
            (tuple): (bool, optional InstallRecord): bool tells us whether
                the spec is installed upstream. Its InstallRecord is also
                returned if it's installed at all; otherwise None.
        """
        if data and hash_key in data:
            return False, data[hash_key]
        if not data:
            with self.read_transaction():
                if hash_key in self._data:
                    return False, self._data[hash_key]
        for db in self.upstream_dbs:
            if hash_key in db._data:
                return True, db._data[hash_key]
        return False, None

    def query_local_by_spec_hash(self, hash_key):
        """Get a spec by hash in the local database

        Return:
            (InstallRecord or None): InstallRecord when installed
                locally, otherwise None."""
        with self.read_transaction():
            return self._data.get(hash_key, None)

    def _assign_dependencies(
        self,
        spec_reader: Type["spack.spec.SpecfileReaderBase"],
        hash_key: str,
        installs: dict,
        data: Dict[str, InstallRecord],
    ):
        # Add dependencies from other records in the install DB to
        # form a full spec.
        spec = data[hash_key].spec
        spec_node_dict = installs[hash_key]["spec"]
        if "name" not in spec_node_dict:
            # old format
            spec_node_dict = spec_node_dict[spec.name]
        if "dependencies" in spec_node_dict:
            yaml_deps = spec_node_dict["dependencies"]
            for dname, dhash, dtypes, _, virtuals in spec_reader.read_specfile_dep_specs(
                yaml_deps
            ):
                # It is important that we always check upstream installations in the same order,
                # and that we always check the local installation first: if a downstream Spack
                # installs a package then dependents in that installation could be using it. If a
                # hash is installed locally and upstream, there isn't enough information to
                # determine which one a local package depends on, so the convention ensures that
                # this isn't an issue.
                _, record = self.query_by_spec_hash(dhash, data=data)
                child = record.spec if record else None

                if not child:
                    tty.warn(
                        f"Missing dependency not in database: "
                        f"{spec.cformat('{name}{/hash:7}')} needs {dname}-{dhash[:7]}"
                    )
                    continue

                spec._add_dependency(child, depflag=dt.canonicalize(dtypes), virtuals=virtuals)

    def _read_from_file(self, filename):
        """Fill database from file, do not maintain old data.
        Translate the spec portions from node-dict form to spec form.

        Does not do any locking.
        """
        try:
            with open(filename, "r") as f:
                # In the future we may use a stream of JSON objects, hence `raw_decode` for compat.
                fdata, _ = JSONDecoder().raw_decode(f.read())
        except Exception as e:
            raise CorruptDatabaseError("error parsing database:", str(e)) from e

        if fdata is None:
            return

        def check(cond, msg):
            if not cond:
                raise CorruptDatabaseError("Spack database is corrupt: %s" % msg, self._index_path)

        check("database" in fdata, "no 'database' attribute in JSON DB.")

        # High-level file checks
        db = fdata["database"]
        check("version" in db, "no 'version' in JSON DB.")

        # TODO: better version checking semantics.
        version = vn.Version(db["version"])
        if version > _DB_VERSION:
            raise InvalidDatabaseVersionError(self, _DB_VERSION, version)
        elif version < _DB_VERSION and not any(
            old == version and new == _DB_VERSION for old, new in _SKIP_REINDEX
        ):
            tty.warn(f"Spack database version changed from {version} to {_DB_VERSION}. Upgrading.")

            self.reindex()
            installs = dict(
                (k, v.to_dict(include_fields=self._record_fields)) for k, v in self._data.items()
            )
        else:
            check("installs" in db, "no 'installs' in JSON DB.")
            installs = db["installs"]

        spec_reader = reader(version)

        def invalid_record(hash_key, error):
            return CorruptDatabaseError(
                f"Invalid record in Spack database: hash: {hash_key}, cause: "
                f"{type(error).__name__}: {error}",
                self._index_path,
            )

        # Build up the database in three passes:
        #
        #   1. Read in all specs without dependencies.
        #   2. Hook dependencies up among specs.
        #   3. Mark all specs concrete.
        #
        # The database is built up so that ALL specs in it share nodes
        # (i.e., its specs are a true Merkle DAG, unlike most specs.)

        # Pass 1: Iterate through database and build specs w/o dependencies
        data: Dict[str, InstallRecord] = {}
        installed_prefixes: Set[str] = set()
        for hash_key, rec in installs.items():
            try:
                # This constructs a spec DAG from the list of all installs
                spec = self._read_spec_from_dict(spec_reader, hash_key, installs)

                # Insert the brand new spec in the database.  Each
                # spec has its own copies of its dependency specs.
                # TODO: would a more immmutable spec implementation simplify
                #       this?
                data[hash_key] = InstallRecord.from_dict(spec, rec)

                if not spec.external and "installed" in rec and rec["installed"]:
                    installed_prefixes.add(rec["path"])
            except Exception as e:
                raise invalid_record(hash_key, e) from e

        # Pass 2: Assign dependencies once all specs are created.
        for hash_key in data:
            try:
                self._assign_dependencies(spec_reader, hash_key, installs, data)
            except MissingDependenciesError:
                raise
            except Exception as e:
                raise invalid_record(hash_key, e) from e

        # Pass 3: Mark all specs concrete.  Specs representing real
        # installations must be explicitly marked.
        # We do this *after* all dependencies are connected because if we
        # do it *while* we're constructing specs,it causes hashes to be
        # cached prematurely.
        for hash_key, rec in data.items():
            rec.spec._mark_root_concrete()

        self._data = data
        self._installed_prefixes = installed_prefixes

    def reindex(self):
        """Build database index from scratch based on a directory layout.

        Locks the DB if it isn't locked already.
        """
        if self.is_upstream:
            raise UpstreamDatabaseLockingError("Cannot reindex an upstream database")

        # Special transaction to avoid recursive reindex calls and to
        # ignore errors if we need to rebuild a corrupt database.
        def _read_suppress_error():
            try:
                if os.path.isfile(self._index_path):
                    self._read_from_file(self._index_path)
            except CorruptDatabaseError as e:
                tty.warn(f"Reindexing corrupt database, error was: {e}")
                self._data = {}
                self._installed_prefixes = set()

        with lk.WriteTransaction(self.lock, acquire=_read_suppress_error, release=self._write):
            old_installed_prefixes, self._installed_prefixes = self._installed_prefixes, set()
            old_data, self._data = self._data, {}
            try:
                self._reindex(old_data)
            except BaseException:
                # If anything explodes, restore old data, skip write.
                self._data = old_data
                self._installed_prefixes = old_installed_prefixes
                raise

    def _reindex(self, old_data: Dict[str, InstallRecord]):
        # Specs on the file system are the source of truth for record.spec. The old database values
        # if available are the source of truth for the rest of the record.
        assert self.layout, "Database layout must be set to reindex"

        specs_from_fs = self.layout.all_specs()
        deprecated_for = self.layout.deprecated_for(specs_from_fs)

        known_specs: List[spack.spec.Spec] = [
            *specs_from_fs,
            *(deprecated for _, deprecated in deprecated_for),
            *(rec.spec for rec in old_data.values()),
        ]

        upstream_hashes = {
            dag_hash for upstream in self.upstream_dbs for dag_hash in upstream._data
        }
        upstream_hashes.difference_update(spec.dag_hash() for spec in known_specs)

        def create_node(edge: spack.spec.DependencySpec, is_upstream: bool):
            if is_upstream:
                return

            self._data[edge.spec.dag_hash()] = InstallRecord(
                spec=edge.spec.copy(deps=False),
                path=edge.spec.external_path if edge.spec.external else None,
                installed=edge.spec.external,
            )

        # Store all nodes of known specs, excluding ones found in upstreams
        tr.traverse_breadth_first_with_visitor(
            known_specs,
            tr.CoverNodesVisitor(
                NoUpstreamVisitor(upstream_hashes, create_node), key=tr.by_dag_hash
            ),
        )

        # Store the prefix and other information for specs were found on the file system
        for s in specs_from_fs:
            record = self._data[s.dag_hash()]
            record.path = s.prefix
            record.installed = True
            record.explicit = True  # conservative assumption
            record.installation_time = os.stat(s.prefix).st_ctime

        # Deprecate specs
        for new, old in deprecated_for:
            self._data[old.dag_hash()].deprecated_for = new.dag_hash()

        # Copy data we have from the old database
        for old_record in old_data.values():
            record = self._data[old_record.spec.dag_hash()]
            record.explicit = old_record.explicit
            record.installation_time = old_record.installation_time
            record.origin = old_record.origin
            record.deprecated_for = old_record.deprecated_for

            # Warn when the spec has been removed from the file system (i.e. it was not detected)
            if not record.installed and old_record.installed:
                tty.warn(
                    f"Spec {old_record.spec.short_spec} was marked installed in the database "
                    "but was not found on the file system. It is now marked as missing."
                )

        def create_edge(edge: spack.spec.DependencySpec, is_upstream: bool):
            if not edge.parent:
                return
            parent_record = self._data[edge.parent.dag_hash()]
            if is_upstream:
                upstream, child_record = self.query_by_spec_hash(edge.spec.dag_hash())
                assert upstream and child_record, "Internal error: upstream spec not found"
            else:
                child_record = self._data[edge.spec.dag_hash()]
            parent_record.spec._add_dependency(
                child_record.spec, depflag=edge.depflag, virtuals=edge.virtuals
            )

        # Then store edges
        tr.traverse_breadth_first_with_visitor(
            known_specs,
            tr.CoverEdgesVisitor(
                NoUpstreamVisitor(upstream_hashes, create_edge), key=tr.by_dag_hash
            ),
        )

        # Finally update the ref counts
        for record in self._data.values():
            for dep in record.spec.dependencies(deptype=_TRACKED_DEPENDENCIES):
                dep_record = self._data.get(dep.dag_hash())
                if dep_record:  # dep might be upstream
                    dep_record.ref_count += 1
            if record.deprecated_for:
                self._data[record.deprecated_for].ref_count += 1

        self._check_ref_counts()

    def _check_ref_counts(self):
        """Ensure consistency of reference counts in the DB.

        Raise an AssertionError if something is amiss.

        Does no locking.
        """
        counts: Dict[str, int] = {}
        for key, rec in self._data.items():
            counts.setdefault(key, 0)
            for dep in rec.spec.dependencies(deptype=_TRACKED_DEPENDENCIES):
                dep_key = dep.dag_hash()
                counts.setdefault(dep_key, 0)
                counts[dep_key] += 1

            if rec.deprecated_for:
                counts.setdefault(rec.deprecated_for, 0)
                counts[rec.deprecated_for] += 1

        for rec in self._data.values():
            key = rec.spec.dag_hash()
            expected = counts[key]
            found = rec.ref_count
            if not expected == found:
                raise AssertionError(
                    "Invalid ref_count: %s: %d (expected %d), in DB %s"
                    % (key, found, expected, self._index_path)
                )

    def _write(self, type, value, traceback):
        """Write the in-memory database index to its file path.

        This is a helper function called by the WriteTransaction context
        manager. If there is an exception while the write lock is active,
        nothing will be written to the database file, but the in-memory
        database *may* be left in an inconsistent state.  It will be consistent
        after the start of the next transaction, when it read from disk again.

        This routine does no locking.
        """
        # Do not write if exceptions were raised
        if type is not None:
            # A failure interrupted a transaction, so we should record that
            # the Database is now in an inconsistent state: we should
            # restore it in the next transaction
            self._state_is_inconsistent = True
            return

        temp_file = self._index_path + (".%s.%s.temp" % (_getfqdn(), os.getpid()))

        # Write a temporary database file them move it into place
        try:
            with open(temp_file, "w") as f:
                self._write_to_file(f)
            fs.rename(temp_file, self._index_path)

            if _use_uuid:
                with open(self._verifier_path, "w") as f:
                    new_verifier = str(uuid.uuid4())
                    f.write(new_verifier)
                    self.last_seen_verifier = new_verifier
        except BaseException as e:
            tty.debug(e)
            # Clean up temp file if something goes wrong.
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise

    def _read(self):
        """Re-read Database from the data in the set location. This does no locking."""
        if os.path.isfile(self._index_path):
            current_verifier = ""
            if _use_uuid:
                try:
                    with open(self._verifier_path, "r") as f:
                        current_verifier = f.read()
                except BaseException:
                    pass
            if (current_verifier != self.last_seen_verifier) or (current_verifier == ""):
                self.last_seen_verifier = current_verifier
                # Read from file if a database exists
                self._read_from_file(self._index_path)
            elif self._state_is_inconsistent:
                self._read_from_file(self._index_path)
                self._state_is_inconsistent = False
            return
        elif self.is_upstream:
            tty.warn("upstream not found: {0}".format(self._index_path))

    def _add(
        self,
        spec: "spack.spec.Spec",
        explicit: bool = False,
        installation_time: Optional[float] = None,
        allow_missing: bool = False,
    ):
        """Add an install record for this spec to the database.

        Also ensures dependencies are present and updated in the DB as either installed or missing.

        Args:
            spec: spec to be added
            explicit:
                Possible values: True, False, any

                A spec that was installed following a specific user request is marked as explicit.
                If instead it was pulled-in as a dependency of a user requested spec it's
                considered implicit.

            installation_time:
                Date and time of installation
            allow_missing: if True, don't warn when installation is not found on on disk
                This is useful when installing specs without build deps.
        """
        if not spec.concrete:
            raise NonConcreteSpecAddError("Specs added to DB must be concrete.")

        key = spec.dag_hash()
        spec_pkg_hash = spec._package_hash  # type: ignore[attr-defined]
        upstream, record = self.query_by_spec_hash(key)
        if upstream:
            return

        installation_time = installation_time or _now()

        for edge in spec.edges_to_dependencies(depflag=_TRACKED_DEPENDENCIES):
            if edge.spec.dag_hash() in self._data:
                continue
            self._add(
                edge.spec,
                explicit=False,
                installation_time=installation_time,
                # allow missing build-only deps. This prevents excessive warnings when a spec is
                # installed, and its build dep is missing a build dep; there's no need to install
                # the build dep's build dep first, and there's no need to warn about it missing.
                allow_missing=allow_missing or edge.depflag == dt.BUILD,
            )

        # Make sure the directory layout agrees whether the spec is installed
        if not spec.external and self.layout:
            path = self.layout.path_for_spec(spec)
            installed = False
            try:
                self.layout.ensure_installed(spec)
                installed = True
                self._installed_prefixes.add(path)
            except DirectoryLayoutError as e:
                if not (allow_missing and isinstance(e, InconsistentInstallDirectoryError)):
                    action = "updated" if key in self._data else "registered"
                    tty.warn(
                        f"{spec.short_spec} is being {action} in the database with prefix {path}, "
                        "but this directory does not contain an installation of "
                        f"the spec, due to: {e}"
                    )
        elif spec.external_path:
            path = spec.external_path
            installed = True
        else:
            path = None
            installed = True

        if key not in self._data:
            # Create a new install record with no deps initially.
            new_spec = spec.copy(deps=False)
            self._data[key] = InstallRecord(
                new_spec,
                path=path,
                installed=installed,
                ref_count=0,
                explicit=explicit,
                installation_time=installation_time,
                origin=None if not hasattr(spec, "origin") else spec.origin,
            )

            # Connect dependencies from the DB to the new copy.
            for dep in spec.edges_to_dependencies(depflag=_TRACKED_DEPENDENCIES):
                dkey = dep.spec.dag_hash()
                upstream, record = self.query_by_spec_hash(dkey)
                assert record, f"Missing dependency {dep.spec.short_spec} in DB"
                new_spec._add_dependency(record.spec, depflag=dep.depflag, virtuals=dep.virtuals)
                if not upstream:
                    record.ref_count += 1

            # Mark concrete once everything is built, and preserve the original hashes of concrete
            # specs.
            new_spec._mark_concrete()
            new_spec._hash = key
            new_spec._package_hash = spec_pkg_hash

        else:
            # It is already in the database
            self._data[key].installed = installed
            self._data[key].installation_time = _now()

        self._data[key].explicit = explicit

    @_autospec
    def add(self, spec: "spack.spec.Spec", *, explicit: bool = False) -> None:
        """Add spec at path to database, locking and reading DB to sync.

        ``add()`` will lock and read from the DB on disk.

        """
        # TODO: ensure that spec is concrete?
        # Entire add is transactional.
        with self.write_transaction():
            self._add(spec, explicit=explicit)

    def _get_matching_spec_key(self, spec: "spack.spec.Spec", **kwargs) -> str:
        """Get the exact spec OR get a single spec that matches."""
        key = spec.dag_hash()
        upstream, record = self.query_by_spec_hash(key)
        if not record:
            match = self.query_one(spec, **kwargs)
            if match:
                return match.dag_hash()
            raise NoSuchSpecError(spec)
        return key

    @_autospec
    def get_record(self, spec: "spack.spec.Spec", **kwargs) -> Optional[InstallRecord]:
        key = self._get_matching_spec_key(spec, **kwargs)
        upstream, record = self.query_by_spec_hash(key)
        return record

    def _decrement_ref_count(self, spec: "spack.spec.Spec") -> None:
        key = spec.dag_hash()

        if key not in self._data:
            # TODO: print something here?  DB is corrupt, but
            # not much we can do.
            return

        rec = self._data[key]
        rec.ref_count -= 1

        if rec.ref_count == 0 and not rec.installed:
            del self._data[key]

            for dep in spec.dependencies(deptype=_TRACKED_DEPENDENCIES):
                self._decrement_ref_count(dep)

    def _increment_ref_count(self, spec: "spack.spec.Spec") -> None:
        key = spec.dag_hash()

        if key not in self._data:
            return

        rec = self._data[key]
        rec.ref_count += 1

    def _remove(self, spec: "spack.spec.Spec") -> "spack.spec.Spec":
        """Non-locking version of remove(); does real work."""
        key = self._get_matching_spec_key(spec)
        rec = self._data[key]

        # This install prefix is now free for other specs to use, even if the
        # spec is only marked uninstalled.
        if not rec.spec.external and rec.installed and rec.path:
            self._installed_prefixes.remove(rec.path)

        if rec.ref_count > 0:
            rec.installed = False
            return rec.spec

        del self._data[key]

        # Remove any reference to this node from dependencies and
        # decrement the reference count
        rec.spec.detach(deptype=_TRACKED_DEPENDENCIES)
        for dep in rec.spec.dependencies(deptype=_TRACKED_DEPENDENCIES):
            self._decrement_ref_count(dep)

        if rec.deprecated_for:
            new_spec = self._data[rec.deprecated_for].spec
            self._decrement_ref_count(new_spec)

        # Returns the concrete spec so we know it in the case where a
        # query spec was passed in.
        return rec.spec

    @_autospec
    def remove(self, spec: "spack.spec.Spec") -> "spack.spec.Spec":
        """Removes a spec from the database.  To be called on uninstall.

        Reads the database, then:

          1. Marks the spec as not installed.
          2. Removes the spec if it has no more dependents.
          3. If removed, recursively updates dependencies' ref counts
             and removes them if they are no longer needed.

        """
        # Take a lock around the entire removal.
        with self.write_transaction():
            return self._remove(spec)

    def deprecator(self, spec: "spack.spec.Spec") -> Optional["spack.spec.Spec"]:
        """Return the spec that the given spec is deprecated for, or None"""
        with self.read_transaction():
            spec_key = self._get_matching_spec_key(spec)
            spec_rec = self._data[spec_key]

            if spec_rec.deprecated_for:
                return self._data[spec_rec.deprecated_for].spec
            else:
                return None

    def specs_deprecated_by(self, spec: "spack.spec.Spec") -> List["spack.spec.Spec"]:
        """Return all specs deprecated in favor of the given spec"""
        with self.read_transaction():
            return [
                rec.spec for rec in self._data.values() if rec.deprecated_for == spec.dag_hash()
            ]

    def _deprecate(self, spec: "spack.spec.Spec", deprecator: "spack.spec.Spec") -> None:
        spec_key = self._get_matching_spec_key(spec)
        spec_rec = self._data[spec_key]

        deprecator_key = self._get_matching_spec_key(deprecator)

        self._increment_ref_count(deprecator)

        # If spec was already deprecated, update old deprecator's ref count
        if spec_rec.deprecated_for:
            old_repl_rec = self._data[spec_rec.deprecated_for]
            self._decrement_ref_count(old_repl_rec.spec)

        spec_rec.deprecated_for = deprecator_key
        spec_rec.installed = False
        self._data[spec_key] = spec_rec

    @_autospec
    def mark(self, spec: "spack.spec.Spec", key, value) -> None:
        """Mark an arbitrary record on a spec."""
        with self.write_transaction():
            return self._mark(spec, key, value)

    def _mark(self, spec: "spack.spec.Spec", key, value) -> None:
        record = self._data[self._get_matching_spec_key(spec)]
        setattr(record, key, value)

    @_autospec
    def deprecate(self, spec: "spack.spec.Spec", deprecator: "spack.spec.Spec") -> None:
        """Marks a spec as deprecated in favor of its deprecator"""
        with self.write_transaction():
            return self._deprecate(spec, deprecator)

    @_autospec
    def installed_relatives(
        self,
        spec: "spack.spec.Spec",
        direction: str = "children",
        transitive: bool = True,
        deptype: Union[dt.DepFlag, dt.DepTypes] = dt.ALL,
    ) -> Set["spack.spec.Spec"]:
        """Return installed specs related to this one."""
        if direction not in ("parents", "children"):
            raise ValueError("Invalid direction: %s" % direction)

        relatives: Set[spack.spec.Spec] = set()
        for spec in self.query(spec):
            if transitive:
                to_add = spec.traverse(direction=direction, root=False, deptype=deptype)
            elif direction == "parents":
                to_add = spec.dependents(deptype=deptype)
            else:  # direction == 'children'
                to_add = spec.dependencies(deptype=deptype)

            for relative in to_add:
                hash_key = relative.dag_hash()
                _, record = self.query_by_spec_hash(hash_key)
                if not record:
                    tty.warn(
                        f"Inconsistent state: "
                        f"{'dependent' if direction == 'parents' else 'dependency'} {hash_key} of "
                        f"{spec.dag_hash()} not in DB"
                    )
                    continue

                if not record.installed:
                    continue

                relatives.add(relative)
        return relatives

    @_autospec
    def installed_extensions_for(self, extendee_spec: "spack.spec.Spec"):
        """Returns the specs of all packages that extend the given spec"""
        for spec in self.query():
            if spec.package.extends(extendee_spec):
                yield spec.package

    def _get_by_hash_local(self, dag_hash, default=None, installed=any):
        # hash is a full hash and is in the data somewhere
        if dag_hash in self._data:
            rec = self._data[dag_hash]
            if rec.install_type_matches(installed):
                return [rec.spec]
            else:
                return default

        # check if hash is a prefix of some installed (or previously
        # installed) spec.
        matches = [
            record.spec
            for h, record in self._data.items()
            if h.startswith(dag_hash) and record.install_type_matches(installed)
        ]
        if matches:
            return matches

        # nothing found
        return default

    def get_by_hash_local(self, dag_hash, default=None, installed=any):
        """Look up a spec in *this DB* by DAG hash, or by a DAG hash prefix.

        Arguments:
            dag_hash (str): hash (or hash prefix) to look up
            default (object or None): default value to return if dag_hash is
                not in the DB (default: None)
            installed (bool or InstallStatus or typing.Iterable or None):
                if ``True``, includes only installed
                specs in the search; if ``False`` only missing specs, and if
                ``any``, all specs in database. If an InstallStatus or iterable
                of InstallStatus, returns specs whose install status
                (installed, deprecated, or missing) matches (one of) the
                InstallStatus. (default: any)

        ``installed`` defaults to ``any`` so that we can refer to any
        known hash.  Note that ``query()`` and ``query_one()`` differ in
        that they only return installed specs by default.

        Returns:
            (list): a list of specs matching the hash or hash prefix

        """
        with self.read_transaction():
            return self._get_by_hash_local(dag_hash, default=default, installed=installed)

    def get_by_hash(self, dag_hash, default=None, installed=any):
        """Look up a spec by DAG hash, or by a DAG hash prefix.

        Arguments:
            dag_hash (str): hash (or hash prefix) to look up
            default (object or None): default value to return if dag_hash is
                not in the DB (default: None)
            installed (bool or InstallStatus or typing.Iterable or None):
                if ``True``, includes only installed specs in the search; if ``False``
                only missing specs, and if ``any``, all specs in database. If an
                InstallStatus or iterable of InstallStatus, returns specs whose install
                status (installed, deprecated, or missing) matches (one of) the
                InstallStatus. (default: any)

        ``installed`` defaults to ``any`` so that we can refer to any
        known hash.  Note that ``query()`` and ``query_one()`` differ in
        that they only return installed specs by default.

        Returns:
            (list): a list of specs matching the hash or hash prefix

        """

        spec = self.get_by_hash_local(dag_hash, default=default, installed=installed)
        if spec is not None:
            return spec

        for upstream_db in self.upstream_dbs:
            spec = upstream_db._get_by_hash_local(dag_hash, default=default, installed=installed)
            if spec is not None:
                return spec

        return default

    def _query(
        self,
        query_spec=any,
        known=any,
        installed=True,
        explicit=any,
        start_date=None,
        end_date=None,
        hashes=None,
        in_buildcache=any,
        origin=None,
    ):
        """Run a query on the database."""

        # TODO: Specs are a lot like queries.  Should there be a
        # TODO: wildcard spec object, and should specs have attributes
        # TODO: like installed and known that can be queried?  Or are
        # TODO: these really special cases that only belong here?

        if query_spec is not any:
            if not isinstance(query_spec, spack.spec.Spec):
                query_spec = spack.spec.Spec(query_spec)

            # Just look up concrete specs with hashes; no fancy search.
            if query_spec.concrete:
                # TODO: handling of hashes restriction is not particularly elegant.
                hash_key = query_spec.dag_hash()
                if hash_key in self._data and (not hashes or hash_key in hashes):
                    return [self._data[hash_key].spec]
                else:
                    return []

        # Abstract specs require more work -- currently we test
        # against everything.
        results = []
        start_date = start_date or datetime.datetime.min
        end_date = end_date or datetime.datetime.max

        # save specs whose name doesn't match for last, to avoid a virtual check
        deferred = []

        for key, rec in self._data.items():
            if hashes is not None and rec.spec.dag_hash() not in hashes:
                continue

            if origin and not (origin == rec.origin):
                continue

            if not rec.install_type_matches(installed):
                continue

            if in_buildcache is not any and rec.in_buildcache != in_buildcache:
                continue

            if explicit is not any and rec.explicit != explicit:
                continue

            if known is not any and known(rec.spec.name):
                continue

            if start_date or end_date:
                inst_date = datetime.datetime.fromtimestamp(rec.installation_time)
                if not (start_date < inst_date < end_date):
                    continue

            if query_spec is any:
                results.append(rec.spec)
                continue

            # check anon specs and exact name matches first
            if not query_spec.name or rec.spec.name == query_spec.name:
                if rec.spec.satisfies(query_spec):
                    results.append(rec.spec)

            # save potential virtual matches for later, but not if we already found a match
            elif not results:
                deferred.append(rec.spec)

        # Checking for virtuals is expensive, so we save it for last and only if needed.
        # If we get here, we didn't find anything in the DB that matched by name.
        # If we did fine something, the query spec can't be virtual b/c we matched an actual
        # package installation, so skip the virtual check entirely. If we *didn't* find anything,
        # check all the deferred specs *if* the query is virtual.
        if not results and query_spec is not any and deferred and query_spec.virtual:
            results = [spec for spec in deferred if spec.satisfies(query_spec)]

        return results

    if _query.__doc__ is None:
        _query.__doc__ = ""
    _query.__doc__ += _QUERY_DOCSTRING

    def query_local(self, *args, **kwargs):
        """Query only the local Spack database.

        This function doesn't guarantee any sorting of the returned
        data for performance reason, since comparing specs for __lt__
        may be an expensive operation.
        """
        with self.read_transaction():
            return self._query(*args, **kwargs)

    if query_local.__doc__ is None:
        query_local.__doc__ = ""
    query_local.__doc__ += _QUERY_DOCSTRING

    def query(self, *args, **kwargs):
        """Query the Spack database including all upstream databases.

        Additional Arguments:
            install_tree (str): query 'all' (default), 'local', 'upstream', or upstream path
        """
        install_tree = kwargs.pop("install_tree", "all")
        valid_trees = ["all", "upstream", "local", self.root] + [u.root for u in self.upstream_dbs]
        if install_tree not in valid_trees:
            msg = "Invalid install_tree argument to Database.query()\n"
            msg += f"Try one of {', '.join(valid_trees)}"
            tty.error(msg)
            return []

        upstream_results = []
        upstreams = self.upstream_dbs
        if install_tree not in ("all", "upstream"):
            upstreams = [u for u in self.upstream_dbs if u.root == install_tree]
        for upstream_db in upstreams:
            # queries for upstream DBs need to *not* lock - we may not
            # have permissions to do this and the upstream DBs won't know about
            # us anyway (so e.g. they should never uninstall specs)
            upstream_results.extend(upstream_db._query(*args, **kwargs) or [])

        local_results = []
        if install_tree in ("all", "local") or self.root == install_tree:
            local_results = set(self.query_local(*args, **kwargs))

        results = list(local_results) + list(x for x in upstream_results if x not in local_results)

        return sorted(results)

    if query.__doc__ is None:
        query.__doc__ = ""
    query.__doc__ += _QUERY_DOCSTRING

    def query_one(self, query_spec, known=any, installed=True):
        """Query for exactly one spec that matches the query spec.

        Raises an assertion error if more than one spec matches the
        query. Returns None if no installed package matches.

        """
        concrete_specs = self.query(query_spec, known=known, installed=installed)
        assert len(concrete_specs) <= 1
        return concrete_specs[0] if concrete_specs else None

    def missing(self, spec):
        key = spec.dag_hash()
        upstream, record = self.query_by_spec_hash(key)
        return record and not record.installed

    def is_occupied_install_prefix(self, path):
        with self.read_transaction():
            return path in self._installed_prefixes

    def all_hashes(self):
        """Return dag hash of every spec in the database."""
        with self.read_transaction():
            return list(self._data.keys())

    def unused_specs(
        self,
        root_hashes: Optional[Container[str]] = None,
        deptype: Union[dt.DepFlag, dt.DepTypes] = dt.LINK | dt.RUN,
    ) -> List["spack.spec.Spec"]:
        """Return all specs that are currently installed but not needed by root specs.

        By default, roots are all explicit specs in the database. If a set of root
        hashes are passed in, they are instead used as the roots.

        Arguments:
            root_hashes: optional list of roots to consider when evaluating needed installations.
            deptype: if a spec is reachable from a root via these dependency types, it is
                considered needed. By default only link and run dependency types are considered.
        """

        def root(key, record):
            """Whether a DB record is a root for garbage collection."""
            return key in root_hashes if root_hashes is not None else record.explicit

        with self.read_transaction():
            roots = [rec.spec for key, rec in self._data.items() if root(key, rec)]
            needed = set(id(spec) for spec in tr.traverse_nodes(roots, deptype=deptype))
            return [
                rec.spec
                for rec in self._data.values()
                if id(rec.spec) not in needed and rec.installed
            ]

    def update_explicit(self, spec, explicit):
        """
        Update the spec's explicit state in the database.

        Args:
            spec (spack.spec.Spec): the spec whose install record is being updated
            explicit (bool): ``True`` if the package was requested explicitly
                by the user, ``False`` if it was pulled in as a dependency of
                an explicit package.
        """
        rec = self.get_record(spec)
        if explicit != rec.explicit:
            with self.write_transaction():
                message = "{s.name}@{s.version} : marking the package {0}"
                status = "explicit" if explicit else "implicit"
                tty.debug(message.format(status, s=spec))
                rec.explicit = explicit


class NoUpstreamVisitor:
    """Gives edges to upstream specs, but does follow edges from upstream specs."""

    def __init__(
        self,
        upstream_hashes: Set[str],
        on_visit: Callable[["spack.spec.DependencySpec", bool], None],
    ):
        self.upstream_hashes = upstream_hashes
        self.on_visit = on_visit

    def accept(self, item: tr.EdgeAndDepth) -> bool:
        self.on_visit(item.edge, self.is_upstream(item))
        return True

    def is_upstream(self, item: tr.EdgeAndDepth) -> bool:
        return item.edge.spec.dag_hash() in self.upstream_hashes

    def neighbors(self, item: tr.EdgeAndDepth):
        # Prune edges from upstream nodes, only follow database tracked dependencies
        return (
            []
            if self.is_upstream(item)
            else item.edge.spec.edges_to_dependencies(depflag=_TRACKED_DEPENDENCIES)
        )


class UpstreamDatabaseLockingError(SpackError):
    """Raised when an operation would need to lock an upstream database"""


class CorruptDatabaseError(SpackError):
    """Raised when errors are found while reading the database."""


class NonConcreteSpecAddError(SpackError):
    """Raised when attempting to add non-concrete spec to DB."""


class MissingDependenciesError(SpackError):
    """Raised when DB cannot find records for dependencies"""


class InvalidDatabaseVersionError(SpackError):
    """Exception raised when the database metadata is newer than current Spack."""

    def __init__(self, database, expected, found):
        self.expected = expected
        self.found = found
        msg = (
            f"you need a newer Spack version to read the DB in '{database.root}'. "
            f"{self.database_version_message}"
        )
        super().__init__(msg)

    @property
    def database_version_message(self):
        return f"The expected DB version is '{self.expected}', but '{self.found}' was found."


class NoSuchSpecError(KeyError):
    """Raised when a spec is not found in the database."""

    def __init__(self, spec):
        self.spec = spec
        super().__init__(spec)

    def __str__(self):
        # This exception is raised frequently, and almost always
        # caught, so ensure we don't pay the cost of Spec.__str__
        # unless the exception is actually printed.
        return f"No such spec in database: {self.spec}"
