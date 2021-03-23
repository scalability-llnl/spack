# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
import six
import socket
import sys
import time
from typing import Dict  # novm

try:
    import uuid
    _use_uuid = True
except ImportError:
    _use_uuid = False
    pass

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.repo
import spack.spec
import spack.store
import spack.util.lock as lk
import spack.util.spack_json as sjson
from spack.directory_layout import DirectoryLayoutError
from spack.error import SpackError
from spack.filesystem_view import YamlFilesystemView
from spack.util.crypto import bit_length
from spack.version import Version


@contextlib.contextmanager
def nullcontext(*args, **kwargs):
    yield


# TODO: Provide an API automatically retyring a build after detecting and
# TODO: clearing a failure.

# DB goes in this directory underneath the root
_db_dirname = '.spack-db'

# DB version.  This is stuck in the DB file to track changes in format.
# Increment by one when the database format changes.
# Versions before 5 were not integers.
_db_version = Version('5')

# For any version combinations here, skip reindex when upgrading.
# Reindexing can take considerable time and is not always necessary.
_skip_reindex = [
    # reindexing takes a significant amount of time, and there's
    # no reason to do it from DB version 0.9.3 to version 5. The
    # only difference is that v5 can contain "deprecated_for"
    # fields.  So, skip the reindex for this transition. The new
    # version is saved to disk the first time the DB is written.
    (Version('0.9.3'), Version('5')),
]

# Default timeout for spack database locks in seconds or None (no timeout).
# A balance needs to be struck between quick turnaround for parallel installs
# (to avoid excess delays) and waiting long enough when the system is busy
# (to ensure the database is updated).
_db_lock_timeout = 120

# Default timeout for spack package locks in seconds or None (no timeout).
# A balance needs to be struck between quick turnaround for parallel installs
# (to avoid excess delays when performing a parallel installation) and waiting
# long enough for the next possible spec to install (to avoid excessive
# checking of the last high priority package) or holding on to a lock (to
# ensure a failed install is properly tracked).
_pkg_lock_timeout = None

# Types of dependencies tracked by the database
_tracked_deps = ('link', 'run')

# Default list of fields written for each install record
default_install_record_fields = [
    'spec',
    'ref_count',
    'path',
    'installed',
    'explicit',
    'installation_time',
    'deprecated_for',
]


def _now():
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


class InstallStatuses(object):
    INSTALLED = InstallStatus('installed')
    DEPRECATED = InstallStatus('deprecated')
    MISSING = InstallStatus('missing')

    @classmethod
    def canonicalize(cls, query_arg):
        if query_arg is True:
            return [cls.INSTALLED]
        elif query_arg is False:
            return [cls.MISSING]
        elif query_arg is any:
            return [cls.INSTALLED, cls.DEPRECATED, cls.MISSING]
        elif isinstance(query_arg, InstallStatus):
            return [query_arg]
        else:
            try:  # Try block catches if it is not an iterable at all
                if any(type(x) != InstallStatus for x in query_arg):
                    raise TypeError
            except TypeError:
                raise TypeError(
                    'installation query must be `any`, boolean, '
                    'InstallStatus, or iterable of InstallStatus')
            return query_arg


class InstallRecord(object):
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
        spec (Spec): spec tracked by the install record
        path (str): path where the spec has been installed
        installed (bool): whether or not the spec is currently installed
        ref_count (int): number of specs that depend on this one
        explicit (bool, optional): whether or not this spec was explicitly
            installed, or pulled-in as a dependency of something else
        installation_time (time, optional): time of the installation
    """

    def __init__(
            self,
            spec,
            path,
            installed,
            ref_count=0,
            explicit=False,
            installation_time=None,
            deprecated_for=None
    ):
        self.spec = spec
        self.path = str(path) if path else None
        self.installed = bool(installed)
        self.ref_count = ref_count
        self.explicit = explicit
        self.installation_time = installation_time or _now()
        self.deprecated_for = deprecated_for

    def install_type_matches(self, installed):
        installed = InstallStatuses.canonicalize(installed)
        if self.installed:
            return InstallStatuses.INSTALLED in installed
        elif self.deprecated_for:
            return InstallStatuses.DEPRECATED in installed
        else:
            return InstallStatuses.MISSING in installed

    def to_dict(self, include_fields=default_install_record_fields):
        rec_dict = {}

        for field_name in include_fields:
            if field_name == 'spec':
                rec_dict.update({'spec': self.spec.node_dict_with_hashes()})
            elif field_name == 'deprecated_for' and self.deprecated_for:
                rec_dict.update({'deprecated_for': self.deprecated_for})
            else:
                rec_dict.update({field_name: getattr(self, field_name)})

        return rec_dict

    @classmethod
    def from_dict(cls, spec, dictionary):
        d = dict(dictionary.items())
        d.pop('spec', None)

        # Old databases may have "None" for path for externals
        if 'path' not in d or d['path'] == 'None':
            d['path'] = None

        if 'installed' not in d:
            d['installed'] = False

        return InstallRecord(spec, **d)


class ForbiddenLockError(SpackError):
    """Raised when an upstream DB attempts to acquire a lock"""


class ForbiddenLock(object):
    def __getattribute__(self, name):
        raise ForbiddenLockError(
            "Cannot access attribute '{0}' of lock".format(name))


_query_docstring = """

        Args:
            query_spec: queries iterate through specs in the database and
                return those that satisfy the supplied ``query_spec``. If
                query_spec is `any`, This will match all specs in the
                database.  If it is a spec, we'll evaluate
                ``spec.satisfies(query_spec)``

            known (bool or any, optional): Specs that are "known" are those
                for which Spack can locate a ``package.py`` file -- i.e.,
                Spack "knows" how to install them.  Specs that are unknown may
                represent packages that existed in a previous version of
                Spack, but have since either changed their name or
                been removed

            installed (bool or any, or InstallStatus or iterable of
                InstallStatus, optional): if ``True``, includes only installed
                specs in the search; if ``False`` only missing specs, and if
                ``any``, all specs in database. If an InstallStatus or iterable
                of InstallStatus, returns specs whose install status
                (installed, deprecated, or missing) matches (one of) the
                InstallStatus. (default: True)

            explicit (bool or any, optional): A spec that was installed
                following a specific user request is marked as explicit. If
                instead it was pulled-in as a dependency of a user requested
                spec it's considered implicit.

            start_date (datetime, optional): filters the query discarding
                specs that have been installed before ``start_date``.

            end_date (datetime, optional): filters the query discarding
                specs that have been installed after ``end_date``.

            hashes (container): list or set of hashes that we can use to
                restrict the search

        Returns:
            list of specs that match the query

        """


class Database(object):

    """Per-process lock objects for each install prefix."""
    _prefix_locks = {}  # type: Dict[str, lk.Lock]

    """Per-process failure (lock) objects for each install prefix."""
    _prefix_failures = {}  # type: Dict[str, lk.Lock]

    def __init__(self, root, db_dir=None, upstream_dbs=None,
                 is_upstream=False, enable_transaction_locking=True,
                 record_fields=default_install_record_fields):
        """Create a Database for Spack installations under ``root``.

        A Database is a cache of Specs data from ``$prefix/spec.yaml``
        files in Spack installation directories.

        By default, Database files (data and lock files) are stored
        under ``root/.spack-db``, which is created if it does not
        exist.  This is the ``db_dir``.

        The Database will attempt to read an ``index.json`` file in
        ``db_dir``.  If that does not exist, it will create a database
        when needed by scanning the entire Database root for ``spec.yaml``
        files according to Spack's ``DirectoryLayout``.

        Caller may optionally provide a custom ``db_dir`` parameter
        where data will be stored. This is intended to be used for
        testing the Database class.

        This class supports writing buildcache index files, in which case
        certain fields are not needed in each install record, and no
        transaction locking is required.  To use this feature, provide
        ``enable_transaction_locking=False``, and specify a list of needed
        fields in ``record_fields``.
        """
        self.root = root

        # If the db_dir is not provided, default to within the db root.
        self._db_dir = db_dir or os.path.join(self.root, _db_dirname)

        # Set up layout of database files within the db dir
        self._index_path = os.path.join(self._db_dir, 'index.json')
        self._verifier_path = os.path.join(self._db_dir, 'index_verifier')
        self._lock_path = os.path.join(self._db_dir, 'lock')

        # This is for other classes to use to lock prefix directories.
        self.prefix_lock_path = os.path.join(self._db_dir, 'prefix_lock')

        # Ensure a persistent location for dealing with parallel installation
        # failures (e.g., across near-concurrent processes).
        self._failure_dir = os.path.join(self._db_dir, 'failures')

        # Support special locks for handling parallel installation failures
        # of a spec.
        self.prefix_fail_path = os.path.join(self._db_dir, 'prefix_failures')

        # Create needed directories and files
        if not os.path.exists(self._db_dir):
            fs.mkdirp(self._db_dir)

        if not os.path.exists(self._failure_dir) and not is_upstream:
            fs.mkdirp(self._failure_dir)

        self.is_upstream = is_upstream
        self.last_seen_verifier = ''

        # initialize rest of state.
        self.db_lock_timeout = (
            spack.config.get('config:db_lock_timeout') or _db_lock_timeout)
        self.package_lock_timeout = (
            spack.config.get('config:package_lock_timeout') or
            _pkg_lock_timeout)
        tty.debug('DATABASE LOCK TIMEOUT: {0}s'.format(
                  str(self.db_lock_timeout)))
        timeout_format_str = ('{0}s'.format(str(self.package_lock_timeout))
                              if self.package_lock_timeout else 'No timeout')
        tty.debug('PACKAGE LOCK TIMEOUT: {0}'.format(
                  str(timeout_format_str)))

        if self.is_upstream:
            self.lock = ForbiddenLock()
        else:
            self.lock = lk.Lock(self._lock_path,
                                default_timeout=self.db_lock_timeout,
                                desc='database')
        self._data = {}

        self.upstream_dbs = list(upstream_dbs) if upstream_dbs else []

        # whether there was an error at the start of a read transaction
        self._error = None

        # For testing: if this is true, an exception is thrown when missing
        # dependencies are detected (rather than just printing a warning
        # message)
        self._fail_when_missing_deps = False

        if enable_transaction_locking:
            self._write_transaction_impl = lk.WriteTransaction
            self._read_transaction_impl = lk.ReadTransaction
        else:
            self._write_transaction_impl = nullcontext
            self._read_transaction_impl = nullcontext

        self._record_fields = record_fields

    def write_transaction(self):
        """Get a write lock context manager for use in a `with` block."""
        return self._write_transaction_impl(
            self.lock, acquire=self._read, release=self._write)

    def read_transaction(self):
        """Get a read lock context manager for use in a `with` block."""
        return self._read_transaction_impl(self.lock, acquire=self._read)

    def _failed_spec_path(self, spec):
        """Return the path to the spec's failure file, which may not exist."""
        if not spec.concrete:
            raise ValueError('Concrete spec required for failure path for {0}'
                             .format(spec.name))

        return os.path.join(self._failure_dir,
                            '{0}-{1}'.format(spec.name, spec.full_hash()))

    def clear_all_failures(self):
        """Force remove install failure tracking files."""
        tty.debug('Releasing prefix failure locks')
        for pkg_id in list(self._prefix_failures.keys()):
            lock = self._prefix_failures.pop(pkg_id, None)
            if lock:
                lock.release_write()

        # Remove all failure markings (aka files)
        tty.debug('Removing prefix failure tracking files')
        for fail_mark in os.listdir(self._failure_dir):
            try:
                os.remove(os.path.join(self._failure_dir, fail_mark))
            except OSError as exc:
                tty.warn('Unable to remove failure marking file {0}: {1}'
                         .format(fail_mark, str(exc)))

    def clear_failure(self, spec, force=False):
        """
        Remove any persistent and cached failure tracking for the spec.

        see `mark_failed()`.

        Args:
            spec (Spec): the spec whose failure indicators are being removed
            force (bool): True if the failure information should be cleared
                when a prefix failure lock exists for the file or False if
                the failure should not be cleared (e.g., it may be
                associated with a concurrent build)

        """
        failure_locked = self.prefix_failure_locked(spec)
        if failure_locked and not force:
            tty.msg('Retaining failure marking for {0} due to lock'
                    .format(spec.name))
            return

        if failure_locked:
            tty.warn('Removing failure marking despite lock for {0}'
                     .format(spec.name))

        lock = self._prefix_failures.pop(spec.prefix, None)
        if lock:
            lock.release_write()

        if self.prefix_failure_marked(spec):
            try:
                path = self._failed_spec_path(spec)
                tty.debug('Removing failure marking for {0}'.format(spec.name))
                os.remove(path)
            except OSError as err:
                tty.warn('Unable to remove failure marking for {0} ({1}): {2}'
                         .format(spec.name, path, str(err)))

    def mark_failed(self, spec):
        """
        Mark a spec as failing to install.

        Prefix failure marking takes the form of a byte range lock on the nth
        byte of a file for coordinating between concurrent parallel build
        processes and a persistent file, named with the full hash and
        containing the spec, in a subdirectory of the database to enable
        persistence across overlapping but separate related build processes.

        The failure lock file, ``spack.store.db.prefix_failures``, lives
        alongside the install DB. ``n`` is the sys.maxsize-bit prefix of the
        associated DAG hash to make the likelihood of collision very low with
        no cleanup required.
        """
        # Dump the spec to the failure file for (manual) debugging purposes
        path = self._failed_spec_path(spec)
        with open(path, 'w') as f:
            spec.to_json(f)

        # Also ensure a failure lock is taken to prevent cleanup removal
        # of failure status information during a concurrent parallel build.
        err = 'Unable to mark {0.name} as failed.'

        prefix = spec.prefix
        if prefix not in self._prefix_failures:
            mark = lk.Lock(
                self.prefix_fail_path,
                start=spec.dag_hash_bit_prefix(bit_length(sys.maxsize)),
                length=1,
                default_timeout=self.package_lock_timeout, desc=spec.name)

            try:
                mark.acquire_write()
            except lk.LockTimeoutError:
                # Unlikely that another process failed to install at the same
                # time but log it anyway.
                tty.debug('PID {0} failed to mark install failure for {1}'
                          .format(os.getpid(), spec.name))
                tty.warn(err.format(spec))

            # Whether we or another process marked it as a failure, track it
            # as such locally.
            self._prefix_failures[prefix] = mark

        return self._prefix_failures[prefix]

    def prefix_failed(self, spec):
        """Return True if the prefix (installation) is marked as failed."""
        # The failure was detected in this process.
        if spec.prefix in self._prefix_failures:
            return True

        # The failure was detected by a concurrent process (e.g., an srun),
        # which is expected to be holding a write lock if that is the case.
        if self.prefix_failure_locked(spec):
            return True

        # Determine if the spec may have been marked as failed by a separate
        # spack build process running concurrently.
        return self.prefix_failure_marked(spec)

    def prefix_failure_locked(self, spec):
        """Return True if a process has a failure lock on the spec."""
        check = lk.Lock(
            self.prefix_fail_path,
            start=spec.dag_hash_bit_prefix(bit_length(sys.maxsize)),
            length=1,
            default_timeout=self.package_lock_timeout, desc=spec.name)

        return check.is_write_locked()

    def prefix_failure_marked(self, spec):
        """Determine if the spec has a persistent failure marking."""
        return os.path.exists(self._failed_spec_path(spec))

    def prefix_lock(self, spec, timeout=None):
        """Get a lock on a particular spec's installation directory.

        NOTE: The installation directory **does not** need to exist.

        Prefix lock is a byte range lock on the nth byte of a file.

        The lock file is ``spack.store.db.prefix_lock`` -- the DB
        tells us what to call it and it lives alongside the install DB.

        n is the sys.maxsize-bit prefix of the DAG hash.  This makes
        likelihood of collision is very low AND it gives us
        readers-writer lock semantics with just a single lockfile, so no
        cleanup required.
        """
        timeout = timeout or self.package_lock_timeout
        prefix = spec.prefix
        if prefix not in self._prefix_locks:
            self._prefix_locks[prefix] = lk.Lock(
                self.prefix_lock_path,
                start=spec.dag_hash_bit_prefix(bit_length(sys.maxsize)),
                length=1,
                default_timeout=timeout, desc=spec.name)
        elif timeout != self._prefix_locks[prefix].default_timeout:
            self._prefix_locks[prefix].default_timeout = timeout

        return self._prefix_locks[prefix]

    @contextlib.contextmanager
    def prefix_read_lock(self, spec):
        prefix_lock = self.prefix_lock(spec)
        prefix_lock.acquire_read()

        try:
            yield self
        except lk.LockError:
            # This addresses the case where a nested lock attempt fails inside
            # of this context manager
            raise
        except (Exception, KeyboardInterrupt):
            prefix_lock.release_read()
            raise
        else:
            prefix_lock.release_read()

    @contextlib.contextmanager
    def prefix_write_lock(self, spec):
        prefix_lock = self.prefix_lock(spec)
        prefix_lock.acquire_write()

        try:
            yield self
        except lk.LockError:
            # This addresses the case where a nested lock attempt fails inside
            # of this context manager
            raise
        except (Exception, KeyboardInterrupt):
            prefix_lock.release_write()
            raise
        else:
            prefix_lock.release_write()

    def _write_to_file(self, stream):
        """Write out the database in JSON format to the stream passed
        as argument.

        This function does not do any locking or transactions.
        """
        # map from per-spec hash code to installation record.
        installs = dict((k, v.to_dict(include_fields=self._record_fields))
                        for k, v in self._data.items())

        # database includes installation list and version.

        # NOTE: this DB version does not handle multiple installs of
        # the same spec well.  If there are 2 identical specs with
        # different paths, it can't differentiate.
        # TODO: fix this before we support multiple install locations.
        database = {
            'database': {
                'installs': installs,
                'version': str(_db_version)
            }
        }

        try:
            sjson.dump(database, stream)
        except (TypeError, ValueError) as e:
            raise sjson.SpackJSONError("error writing JSON database:", str(e))

    def _read_spec_from_dict(self, hash_key, installs):
        """Recursively construct a spec from a hash in a YAML database.

        Does not do any locking.
        """
        spec_dict = installs[hash_key]['spec']

        # Install records don't include hash with spec, so we add it in here
        # to ensure it is read properly.
        for name in spec_dict:
            spec_dict[name]['hash'] = hash_key

        # Build spec from dict first.
        spec = spack.spec.Spec.from_node_dict(spec_dict)
        return spec

    def db_for_spec_hash(self, hash_key):
        with self.read_transaction():
            if hash_key in self._data:
                return self

        for db in self.upstream_dbs:
            if hash_key in db._data:
                return db

    def query_by_spec_hash(self, hash_key, data=None):
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

    def _assign_dependencies(self, hash_key, installs, data):
        # Add dependencies from other records in the install DB to
        # form a full spec.
        spec = data[hash_key].spec
        spec_dict = installs[hash_key]['spec']
        if 'dependencies' in spec_dict[spec.name]:
            yaml_deps = spec_dict[spec.name]['dependencies']
            for dname, dhash, dtypes in spack.spec.Spec.read_yaml_dep_specs(
                    yaml_deps):
                # It is important that we always check upstream installations
                # in the same order, and that we always check the local
                # installation first: if a downstream Spack installs a package
                # then dependents in that installation could be using it.
                # If a hash is installed locally and upstream, there isn't
                # enough information to determine which one a local package
                # depends on, so the convention ensures that this isn't an
                # issue.
                upstream, record = self.query_by_spec_hash(dhash, data=data)
                child = record.spec if record else None

                if not child:
                    msg = ("Missing dependency not in database: "
                           "%s needs %s-%s" % (
                               spec.cformat('{name}{/hash:7}'),
                               dname, dhash[:7]))
                    if self._fail_when_missing_deps:
                        raise MissingDependenciesError(msg)
                    tty.warn(msg)
                    continue

                spec._add_dependency(child, dtypes)

    def _read_from_file(self, filename):
        """Fill database from file, do not maintain old data.
        Translate the spec portions from node-dict form to spec form.

        Does not do any locking.
        """
        try:
            with open(filename, 'r') as f:
                fdata = sjson.load(f)
        except Exception as e:
            raise CorruptDatabaseError("error parsing database:", str(e))

        if fdata is None:
            return

        def check(cond, msg):
            if not cond:
                raise CorruptDatabaseError(
                    "Spack database is corrupt: %s" % msg, self._index_path)

        check('database' in fdata, "no 'database' attribute in JSON DB.")

        # High-level file checks
        db = fdata['database']
        check('installs' in db, "no 'installs' in JSON DB.")
        check('version' in db, "no 'version' in JSON DB.")

        installs = db['installs']

        # TODO: better version checking semantics.
        version = Version(db['version'])
        if version > _db_version:
            raise InvalidDatabaseVersionError(_db_version, version)
        elif version < _db_version:
            if not any(
                    old == version and new == _db_version
                    for old, new in _skip_reindex
            ):
                tty.warn(
                    "Spack database version changed from %s to %s. Upgrading."
                    % (version, _db_version)
                )

                self.reindex(spack.store.layout)
                installs = dict(
                    (k, v.to_dict(include_fields=self._record_fields))
                    for k, v in self._data.items()
                )

        def invalid_record(hash_key, error):
            msg = ("Invalid record in Spack database: "
                   "hash: %s, cause: %s: %s")
            msg %= (hash_key, type(error).__name__, str(error))
            raise CorruptDatabaseError(msg, self._index_path)

        # Build up the database in three passes:
        #
        #   1. Read in all specs without dependencies.
        #   2. Hook dependencies up among specs.
        #   3. Mark all specs concrete.
        #
        # The database is built up so that ALL specs in it share nodes
        # (i.e., its specs are a true Merkle DAG, unlike most specs.)

        # Pass 1: Iterate through database and build specs w/o dependencies
        data = {}
        for hash_key, rec in installs.items():
            try:
                # This constructs a spec DAG from the list of all installs
                spec = self._read_spec_from_dict(hash_key, installs)

                # Insert the brand new spec in the database.  Each
                # spec has its own copies of its dependency specs.
                # TODO: would a more immmutable spec implementation simplify
                #       this?
                data[hash_key] = InstallRecord.from_dict(spec, rec)
            except Exception as e:
                invalid_record(hash_key, e)

        # Pass 2: Assign dependencies once all specs are created.
        for hash_key in data:
            try:
                self._assign_dependencies(hash_key, installs, data)
            except MissingDependenciesError:
                raise
            except Exception as e:
                invalid_record(hash_key, e)

        # Pass 3: Mark all specs concrete.  Specs representing real
        # installations must be explicitly marked.
        # We do this *after* all dependencies are connected because if we
        # do it *while* we're constructing specs,it causes hashes to be
        # cached prematurely.
        for hash_key, rec in data.items():
            rec.spec._mark_root_concrete()

        self._data = data

    def reindex(self, directory_layout):
        """Build database index from scratch based on a directory layout.

        Locks the DB if it isn't locked already.
        """
        if self.is_upstream:
            raise UpstreamDatabaseLockingError(
                "Cannot reindex an upstream database")

        # Special transaction to avoid recursive reindex calls and to
        # ignore errors if we need to rebuild a corrupt database.
        def _read_suppress_error():
            try:
                if os.path.isfile(self._index_path):
                    self._read_from_file(self._index_path)
            except CorruptDatabaseError as e:
                self._error = e
                self._data = {}

        transaction = lk.WriteTransaction(
            self.lock, acquire=_read_suppress_error, release=self._write
        )

        with transaction:
            if self._error:
                tty.warn(
                    "Spack database was corrupt. Will rebuild. Error was:",
                    str(self._error)
                )
                self._error = None

            old_data = self._data
            try:
                self._construct_from_directory_layout(
                    directory_layout, old_data)
            except BaseException:
                # If anything explodes, restore old data, skip write.
                self._data = old_data
                raise

    def _construct_entry_from_directory_layout(self, directory_layout,
                                               old_data, spec,
                                               deprecator=None):
        # Try to recover explicit value from old DB, but
        # default it to True if DB was corrupt. This is
        # just to be conservative in case a command like
        # "autoremove" is run by the user after a reindex.
        tty.debug(
            'RECONSTRUCTING FROM SPEC.YAML: {0}'.format(spec))
        explicit = True
        inst_time = os.stat(spec.prefix).st_ctime
        if old_data is not None:
            old_info = old_data.get(spec.dag_hash())
            if old_info is not None:
                explicit = old_info.explicit
                inst_time = old_info.installation_time

        extra_args = {
            'explicit': explicit,
            'installation_time': inst_time
        }
        self._add(spec, directory_layout, **extra_args)
        if deprecator:
            self._deprecate(spec, deprecator)

    def _construct_from_directory_layout(self, directory_layout, old_data):
        # Read first the `spec.yaml` files in the prefixes. They should be
        # considered authoritative with respect to DB reindexing, as
        # entries in the DB may be corrupted in a way that still makes
        # them readable. If we considered DB entries authoritative
        # instead, we would perpetuate errors over a reindex.
        with directory_layout.disable_upstream_check():
            # Initialize data in the reconstructed DB
            self._data = {}

            # Start inspecting the installed prefixes
            processed_specs = set()

            for spec in directory_layout.all_specs():
                self._construct_entry_from_directory_layout(directory_layout,
                                                            old_data, spec)
                processed_specs.add(spec)

            for spec, deprecator in directory_layout.all_deprecated_specs():
                self._construct_entry_from_directory_layout(directory_layout,
                                                            old_data, spec,
                                                            deprecator)
                processed_specs.add(spec)

            for key, entry in old_data.items():
                # We already took care of this spec using
                # `spec.yaml` from its prefix.
                if entry.spec in processed_specs:
                    msg = 'SKIPPING RECONSTRUCTION FROM OLD DB: {0}'
                    msg += ' [already reconstructed from spec.yaml]'
                    tty.debug(msg.format(entry.spec))
                    continue

                # If we arrived here it very likely means that
                # we have external specs that are not dependencies
                # of other specs. This may be the case for externally
                # installed compilers or externally installed
                # applications.
                tty.debug(
                    'RECONSTRUCTING FROM OLD DB: {0}'.format(entry.spec))
                try:
                    layout = spack.store.layout
                    if entry.spec.external:
                        layout = None
                        install_check = True
                    else:
                        install_check = layout.check_installed(entry.spec)

                    if install_check:
                        kwargs = {
                            'spec': entry.spec,
                            'directory_layout': layout,
                            'explicit': entry.explicit,
                            'installation_time': entry.installation_time  # noqa: E501
                        }
                        self._add(**kwargs)
                        processed_specs.add(entry.spec)
                except Exception as e:
                    # Something went wrong, so the spec was not restored
                    # from old data
                    tty.debug(e)

            self._check_ref_counts()

    def _check_ref_counts(self):
        """Ensure consistency of reference counts in the DB.

        Raise an AssertionError if something is amiss.

        Does no locking.
        """
        counts = {}
        for key, rec in self._data.items():
            counts.setdefault(key, 0)
            for dep in rec.spec.dependencies(_tracked_deps):
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
                    "Invalid ref_count: %s: %d (expected %d), in DB %s" %
                    (key, found, expected, self._index_path))

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
            return

        temp_file = self._index_path + (
            '.%s.%s.temp' % (socket.getfqdn(), os.getpid()))

        # Write a temporary database file them move it into place
        try:
            with open(temp_file, 'w') as f:
                self._write_to_file(f)
            os.rename(temp_file, self._index_path)
            if _use_uuid:
                with open(self._verifier_path, 'w') as f:
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
        """Re-read Database from the data in the set location.

        This does no locking, with one exception: it will automatically
        try to regenerate a missing DB if local. This requires taking a
        write lock.
        """
        if os.path.isfile(self._index_path):
            current_verifier = ''
            if _use_uuid:
                try:
                    with open(self._verifier_path, 'r') as f:
                        current_verifier = f.read()
                except BaseException:
                    pass
            if ((current_verifier != self.last_seen_verifier) or
                    (current_verifier == '')):
                self.last_seen_verifier = current_verifier
                # Read from file if a database exists
                self._read_from_file(self._index_path)
            return
        elif self.is_upstream:
            raise UpstreamDatabaseLockingError(
                "No database index file is present, and upstream"
                " databases cannot generate an index file")

        # The file doesn't exist, try to traverse the directory.
        # reindex() takes its own write lock, so no lock here.
        with lk.WriteTransaction(self.lock):
            self._write(None, None, None)
        self.reindex(spack.store.layout)

    def _add(
            self,
            spec,
            directory_layout=None,
            explicit=False,
            installation_time=None
    ):
        """Add an install record for this spec to the database.

        Assumes spec is installed in ``layout.path_for_spec(spec)``.

        Also ensures dependencies are present and updated in the DB as
        either installed or missing.

        Args:
            spec: spec to be added
            directory_layout: layout of the spec installation
            **kwargs:

                explicit
                    Possible values: True, False, any

                    A spec that was installed following a specific user
                    request is marked as explicit. If instead it was
                    pulled-in as a dependency of a user requested spec
                    it's considered implicit.

                installation_time
                    Date and time of installation

        """
        if not spec.concrete:
            raise NonConcreteSpecAddError(
                "Specs added to DB must be concrete.")

        key = spec.dag_hash()
        upstream, record = self.query_by_spec_hash(key)
        if upstream:
            return

        # Retrieve optional arguments
        installation_time = installation_time or _now()

        for dep in spec.dependencies(_tracked_deps):
            dkey = dep.dag_hash()
            if dkey not in self._data:
                extra_args = {
                    'explicit': False,
                    'installation_time': installation_time
                }
                self._add(dep, directory_layout, **extra_args)

        if key not in self._data:
            installed = bool(spec.external)
            path = None
            if not spec.external and directory_layout:
                path = directory_layout.path_for_spec(spec)
                try:
                    directory_layout.check_installed(spec)
                    installed = True
                except DirectoryLayoutError as e:
                    tty.warn(
                        'Dependency missing: may be deprecated or corrupted:',
                        path, str(e))
            elif spec.external_path:
                path = spec.external_path

            # Create a new install record with no deps initially.
            new_spec = spec.copy(deps=False)
            extra_args = {
                'explicit': explicit,
                'installation_time': installation_time
            }
            self._data[key] = InstallRecord(
                new_spec, path, installed, ref_count=0, **extra_args
            )

            # Connect dependencies from the DB to the new copy.
            for name, dep in six.iteritems(
                    spec.dependencies_dict(_tracked_deps)
            ):
                dkey = dep.spec.dag_hash()
                upstream, record = self.query_by_spec_hash(dkey)
                new_spec._add_dependency(record.spec, dep.deptypes)
                if not upstream:
                    record.ref_count += 1

            # Mark concrete once everything is built, and preserve
            # the original hash of concrete specs.
            new_spec._mark_concrete()
            new_spec._hash = key
            new_spec._full_hash = spec._full_hash

        else:
            # If it is already there, mark it as installed and update
            # installation time
            self._data[key].installed = True
            self._data[key].installation_time = _now()

        self._data[key].explicit = explicit

    @_autospec
    def add(self, spec, directory_layout, explicit=False):
        """Add spec at path to database, locking and reading DB to sync.

        ``add()`` will lock and read from the DB on disk.

        """
        # TODO: ensure that spec is concrete?
        # Entire add is transactional.
        with self.write_transaction():
            self._add(spec, directory_layout, explicit=explicit)

    def _get_matching_spec_key(self, spec, **kwargs):
        """Get the exact spec OR get a single spec that matches."""
        key = spec.dag_hash()
        upstream, record = self.query_by_spec_hash(key)
        if not record:
            match = self.query_one(spec, **kwargs)
            if match:
                return match.dag_hash()
            raise KeyError("No such spec in database! %s" % spec)
        return key

    @_autospec
    def get_record(self, spec, **kwargs):
        key = self._get_matching_spec_key(spec, **kwargs)
        upstream, record = self.query_by_spec_hash(key)
        return record

    def _decrement_ref_count(self, spec):
        key = spec.dag_hash()

        if key not in self._data:
            # TODO: print something here?  DB is corrupt, but
            # not much we can do.
            return

        rec = self._data[key]
        rec.ref_count -= 1

        if rec.ref_count == 0 and not rec.installed:
            del self._data[key]
            for dep in spec.dependencies(_tracked_deps):
                self._decrement_ref_count(dep)

    def _increment_ref_count(self, spec):
        key = spec.dag_hash()

        if key not in self._data:
            return

        rec = self._data[key]
        rec.ref_count += 1

    def _remove(self, spec):
        """Non-locking version of remove(); does real work."""
        key = self._get_matching_spec_key(spec)
        rec = self._data[key]

        if rec.ref_count > 0:
            rec.installed = False
            return rec.spec

        del self._data[key]
        for dep in rec.spec.dependencies(_tracked_deps):
            # FIXME: the two lines below needs to be updated once #11983 is
            # FIXME: fixed. The "if" statement should be deleted and specs are
            # FIXME: to be removed from dependents by hash and not by name.
            # FIXME: See https://github.com/spack/spack/pull/15777#issuecomment-607818955
            if dep._dependents.get(spec.name):
                del dep._dependents[spec.name]
            self._decrement_ref_count(dep)

        if rec.deprecated_for:
            new_spec = self._data[rec.deprecated_for].spec
            self._decrement_ref_count(new_spec)

        # Returns the concrete spec so we know it in the case where a
        # query spec was passed in.
        return rec.spec

    @_autospec
    def remove(self, spec):
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

    def deprecator(self, spec):
        """Return the spec that the given spec is deprecated for, or None"""
        with self.read_transaction():
            spec_key = self._get_matching_spec_key(spec)
            spec_rec = self._data[spec_key]

            if spec_rec.deprecated_for:
                return self._data[spec_rec.deprecated_for].spec
            else:
                return None

    def specs_deprecated_by(self, spec):
        """Return all specs deprecated in favor of the given spec"""
        with self.read_transaction():
            return [rec.spec for rec in self._data.values()
                    if rec.deprecated_for == spec.dag_hash()]

    def _deprecate(self, spec, deprecator):
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
    def deprecate(self, spec, deprecator):
        """Marks a spec as deprecated in favor of its deprecator"""
        with self.write_transaction():
            return self._deprecate(spec, deprecator)

    @_autospec
    def installed_relatives(self, spec, direction='children', transitive=True,
                            deptype='all'):
        """Return installed specs related to this one."""
        if direction not in ('parents', 'children'):
            raise ValueError("Invalid direction: %s" % direction)

        relatives = set()
        for spec in self.query(spec):
            if transitive:
                to_add = spec.traverse(
                    direction=direction, root=False, deptype=deptype)
            elif direction == 'parents':
                to_add = spec.dependents(deptype=deptype)
            else:  # direction == 'children'
                to_add = spec.dependencies(deptype=deptype)

            for relative in to_add:
                hash_key = relative.dag_hash()
                upstream, record = self.query_by_spec_hash(hash_key)
                if not record:
                    reltype = ('Dependent' if direction == 'parents'
                               else 'Dependency')
                    msg = ("Inconsistent state! %s %s of %s not in DB"
                           % (reltype, hash_key, spec.dag_hash()))
                    if self._fail_when_missing_deps:
                        raise MissingDependenciesError(msg)
                    tty.warn(msg)
                    continue

                if not record.installed:
                    continue

                relatives.add(relative)
        return relatives

    @_autospec
    def installed_extensions_for(self, extendee_spec):
        """
        Return the specs of all packages that extend
        the given spec
        """
        for spec in self.query():
            if spec.package.extends(extendee_spec):
                yield spec.package

    @_autospec
    def activated_extensions_for(self, extendee_spec, extensions_layout=None):
        """
        Return the specs of all packages that extend
        the given spec
        """
        if extensions_layout is None:
            view = YamlFilesystemView(extendee_spec.prefix, spack.store.layout)
            extensions_layout = view.extensions_layout
        for spec in self.query():
            try:
                extensions_layout.check_activated(extendee_spec, spec)
                yield spec.package
            except spack.directory_layout.NoSuchExtensionError:
                continue
            # TODO: conditional way to do this instead of catching exceptions

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
        matches = [record.spec for h, record in self._data.items()
                   if h.startswith(dag_hash) and
                   record.install_type_matches(installed)]
        if matches:
            return matches

        # nothing found
        return default

    def get_by_hash_local(self, *args, **kwargs):
        """Look up a spec in *this DB* by DAG hash, or by a DAG hash prefix.

        Arguments:
            dag_hash (str): hash (or hash prefix) to look up
            default (object, optional): default value to return if dag_hash is
                not in the DB (default: None)
            installed (bool or any, or InstallStatus or iterable of
                InstallStatus, optional): if ``True``, includes only installed
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
            return self._get_by_hash_local(*args, **kwargs)

    def get_by_hash(self, dag_hash, default=None, installed=any):
        """Look up a spec by DAG hash, or by a DAG hash prefix.

        Arguments:
            dag_hash (str): hash (or hash prefix) to look up
            default (object, optional): default value to return if dag_hash is
                not in the DB (default: None)
            installed (bool or any, or InstallStatus or iterable of
                InstallStatus, optional): if ``True``, includes only installed
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

        spec = self.get_by_hash_local(
            dag_hash, default=default, installed=installed)
        if spec is not None:
            return spec

        for upstream_db in self.upstream_dbs:
            spec = upstream_db._get_by_hash_local(
                dag_hash, default=default, installed=installed)
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
            hashes=None
    ):
        """Run a query on the database."""

        # TODO: Specs are a lot like queries.  Should there be a
        # TODO: wildcard spec object, and should specs have attributes
        # TODO: like installed and known that can be queried?  Or are
        # TODO: these really special cases that only belong here?

        # Just look up concrete specs with hashes; no fancy search.
        if isinstance(query_spec, spack.spec.Spec) and query_spec.concrete:
            # TODO: handling of hashes restriction is not particularly elegant.
            hash_key = query_spec.dag_hash()
            if (hash_key in self._data and
                    (not hashes or hash_key in hashes)):
                return [self._data[hash_key].spec]
            else:
                return []

        # Abstract specs require more work -- currently we test
        # against everything.
        results = []
        start_date = start_date or datetime.datetime.min
        end_date = end_date or datetime.datetime.max

        for key, rec in self._data.items():
            if hashes is not None and rec.spec.dag_hash() not in hashes:
                continue

            if not rec.install_type_matches(installed):
                continue

            if explicit is not any and rec.explicit != explicit:
                continue

            if known is not any and spack.repo.path.exists(
                    rec.spec.name) != known:
                continue

            if start_date or end_date:
                inst_date = datetime.datetime.fromtimestamp(
                    rec.installation_time
                )
                if not (start_date < inst_date < end_date):
                    continue

            if (query_spec is any or
                rec.spec.satisfies(query_spec, strict=True)):
                results.append(rec.spec)

        return results

    if _query.__doc__ is None:
        _query.__doc__ = ""
    _query.__doc__ += _query_docstring

    def query_local(self, *args, **kwargs):
        """Query only the local Spack database."""
        with self.read_transaction():
            return sorted(self._query(*args, **kwargs))

    if query_local.__doc__ is None:
        query_local.__doc__ = ""
    query_local.__doc__ += _query_docstring

    def query(self, *args, **kwargs):
        """Query the Spack database including all upstream databases."""
        upstream_results = []
        for upstream_db in self.upstream_dbs:
            # queries for upstream DBs need to *not* lock - we may not
            # have permissions to do this and the upstream DBs won't know about
            # us anyway (so e.g. they should never uninstall specs)
            upstream_results.extend(upstream_db._query(*args, **kwargs) or [])

        local_results = set(self.query_local(*args, **kwargs))

        results = list(local_results) + list(
            x for x in upstream_results if x not in local_results)

        return sorted(results)

    if query.__doc__ is None:
        query.__doc__ = ""
    query.__doc__ += _query_docstring

    def query_one(self, query_spec, known=any, installed=True):
        """Query for exactly one spec that matches the query spec.

        Raises an assertion error if more than one spec matches the
        query. Returns None if no installed package matches.

        """
        concrete_specs = self.query(
            query_spec, known=known, installed=installed)
        assert len(concrete_specs) <= 1
        return concrete_specs[0] if concrete_specs else None

    def missing(self, spec):
        key = spec.dag_hash()
        upstream, record = self.query_by_spec_hash(key)
        return record and not record.installed

    @property
    def unused_specs(self):
        """Return all the specs that are currently installed but not needed
        at runtime to satisfy user's requests.

        Specs in the return list are those which are not either:
            1. Installed on an explicit user request
            2. Installed as a "run" or "link" dependency (even transitive) of
               a spec at point 1.
        """
        needed, visited = set(), set()
        with self.read_transaction():
            for key, rec in self._data.items():
                if rec.explicit:
                    # recycle `visited` across calls to avoid
                    # redundantly traversing
                    for spec in rec.spec.traverse(visited=visited):
                        needed.add(spec.dag_hash())

            unused = [rec.spec for key, rec in self._data.items()
                      if key not in needed and rec.installed]

        return unused

    def update_explicit(self, spec, explicit):
        """
        Update the spec's explicit state in the database.

        Args:
            spec (Spec): the spec whose install record is being updated
            explicit (bool): ``True`` if the package was requested explicitly
                by the user, ``False`` if it was pulled in as a dependency of
                an explicit package.
        """
        rec = self.get_record(spec)
        if explicit != rec.explicit:
            with self.write_transaction():
                message = '{s.name}@{s.version} : marking the package {0}'
                status = 'explicit' if explicit else 'implicit'
                tty.debug(message.format(status, s=spec))
                rec.explicit = explicit


class UpstreamDatabaseLockingError(SpackError):
    """Raised when an operation would need to lock an upstream database"""


class CorruptDatabaseError(SpackError):
    """Raised when errors are found while reading the database."""


class NonConcreteSpecAddError(SpackError):
    """Raised when attemptint to add non-concrete spec to DB."""


class MissingDependenciesError(SpackError):
    """Raised when DB cannot find records for dependencies"""


class InvalidDatabaseVersionError(SpackError):

    def __init__(self, expected, found):
        super(InvalidDatabaseVersionError, self).__init__(
            "Expected database version %s but found version %s."
            % (expected, found),
            "`spack reindex` may fix this, or you may need a newer "
            "Spack version.")
