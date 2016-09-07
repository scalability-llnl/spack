##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Spack's installation tracking database.

The database serves two purposes:

  1. It implements a cache on top of a potentially very large Spack
     directory hierarchy, speeding up many operations that would
     otherwise require filesystem access.

  2. It will allow us to track external installations as well as lost
     packages and their dependencies.

Prior ot the implementation of this store, a direcotry layout served
as the authoritative database of packages in Spack.  This module
provides a cache and a sanity checking mechanism for what is in the
filesystem.

"""
import os
import socket

from yaml.error import MarkedYAMLError, YAMLError

import llnl.util.tty as tty
from llnl.util.filesystem import *
from llnl.util.lock import *

import spack.spec
from spack.version import Version
from spack.spec import Spec
from spack.error import SpackError
from spack.repository import UnknownPackageError
import spack.util.spack_yaml as syaml

# DB goes in this directory underneath the root
_db_dirname = '.spack-db'

# DB version.  This is stuck in the DB file to track changes in format.
_db_version = Version('0.9.2')

# Default timeout for spack database locks is 5 min.
_db_lock_timeout = 60


def _autospec(function):
    """Decorator that automatically converts the argument of a single-arg
       function to a Spec."""

    def converter(self, spec_like, *args, **kwargs):
        if not isinstance(spec_like, spack.spec.Spec):
            spec_like = spack.spec.Spec(spec_like)
        return function(self, spec_like, *args, **kwargs)

    return converter


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

    """

    def __init__(self, spec, path, installed, ref_count=0, explicit=False):
        self.spec = spec
        self.path = str(path)
        self.installed = bool(installed)
        self.ref_count = ref_count
        self.explicit = explicit

    def to_dict(self):
        return {
            'spec': self.spec.to_node_dict(),
            'path': self.path,
            'installed': self.installed,
            'ref_count': self.ref_count,
            'explicit': self.explicit
        }

    @classmethod
    def from_dict(cls, spec, dictionary):
        d = dictionary
        return InstallRecord(spec, d['path'], d['installed'], d['ref_count'],
                             d.get('explicit', False))


class Database(object):

    def __init__(self, root, db_dir=None):
        """Create a Database for Spack installations under ``root``.

        A Database is a cache of Specs data from ``$prefix/spec.yaml``
        files in Spack installation directories.

        By default, Database files (data and lock files) are stored
        under ``root/.spack-db``, which is created if it does not
        exist.  This is the ``db_dir``.

        The Database will attempt to read an ``index.yaml`` file in
        ``db_dir``.  If it does not find one, it will be created when
        needed by scanning the entire Database root for ``spec.yaml``
        files according to Spack's ``DirectoryLayout``.

        Caller may optionally provide a custom ``db_dir`` parameter
        where data will be stored.  This is intended to be used for
        testing the Database class.

        """
        self.root = root

        if db_dir is None:
            # If the db_dir is not provided, default to within the db root.
            self._db_dir = join_path(self.root, _db_dirname)
        else:
            # Allow customizing the database directory location for testing.
            self._db_dir = db_dir

        # Set up layout of database files within the db dir
        self._index_path = join_path(self._db_dir, 'index.yaml')
        self._lock_path = join_path(self._db_dir, 'lock')

        # Create needed directories and files
        if not os.path.exists(self._db_dir):
            mkdirp(self._db_dir)

        if not os.path.exists(self._lock_path):
            touch(self._lock_path)

        # initialize rest of state.
        self.lock = Lock(self._lock_path)
        self._data = {}

        # whether there was an error at the start of a read transaction
        self._error = None

    def write_transaction(self, timeout=_db_lock_timeout):
        """Get a write lock context manager for use in a `with` block."""
        return WriteTransaction(self.lock, self._read, self._write, timeout)

    def read_transaction(self, timeout=_db_lock_timeout):
        """Get a read lock context manager for use in a `with` block."""
        return ReadTransaction(self.lock, self._read, timeout=timeout)

    def _write_to_yaml(self, stream):
        """Write out the databsae to a YAML file.

        This function does not do any locking or transactions.
        """
        # map from per-spec hash code to installation record.
        installs = dict((k, v.to_dict()) for k, v in self._data.items())

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
            return syaml.dump(
                database, stream=stream, default_flow_style=False)
        except YAMLError as e:
            raise SpackYAMLError("error writing YAML database:", str(e))

    def _read_spec_from_yaml(self, hash_key, installs):
        """Recursively construct a spec from a hash in a YAML database.

        Does not do any locking.
        """
        spec_dict = installs[hash_key]['spec']

        # Install records don't include hash with spec, so we add it in here
        # to ensure it is read properly.
        for name in spec_dict:
            spec_dict[name]['hash'] = hash_key

        # Build spec from dict first.
        spec = Spec.from_node_dict(spec_dict)
        return spec

    def _assign_dependencies(self, hash_key, installs, data):
        # Add dependencies from other records in the install DB to
        # form a full spec.
        spec = data[hash_key].spec
        spec_dict = installs[hash_key]['spec']

        if 'dependencies' in spec_dict[spec.name]:
            yaml_deps = spec_dict[spec.name]['dependencies']
            for dname, dhash, dtypes in Spec.read_yaml_dep_specs(yaml_deps):
                if dhash not in data:
                    tty.warn("Missing dependency not in database: ",
                             "%s needs %s-%s" % (
                                 spec.format('$_$#'), dname, dhash[:7]))
                    continue

                # defensive copy (not sure everything handles extra
                # parent links yet)
                child = data[dhash].spec
                spec._add_dependency(child, dtypes)

    def _read_from_yaml(self, stream):
        """
        Fill database from YAML, do not maintain old data
        Translate the spec portions from node-dict form to spec form

        Does not do any locking.
        """
        try:
            if isinstance(stream, basestring):
                with open(stream, 'r') as f:
                    yfile = syaml.load(f)
            else:
                yfile = syaml.load(stream)

        except MarkedYAMLError as e:
            raise SpackYAMLError("error parsing YAML database:", str(e))

        if yfile is None:
            return

        def check(cond, msg):
            if not cond:
                raise CorruptDatabaseError(
                    "Spack database is corrupt: %s" % msg, self._index_path)

        check('database' in yfile, "No 'database' attribute in YAML.")

        # High-level file checks
        db = yfile['database']
        check('installs' in db, "No 'installs' in YAML DB.")
        check('version' in db, "No 'version' in YAML DB.")

        installs = db['installs']

        # TODO: better version checking semantics.
        version = Version(db['version'])
        if version > _db_version:
            raise InvalidDatabaseVersionError(_db_version, version)
        elif version < _db_version:
            self.reindex(spack.install_layout)
            installs = dict((k, v.to_dict()) for k, v in self._data.items())

        def invalid_record(hash_key, error):
            msg = ("Invalid record in Spack database: "
                   "hash: %s, cause: %s: %s")
            msg %= (hash_key, type(e).__name__, str(e))
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
                spec = self._read_spec_from_yaml(hash_key, installs)

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
            except Exception as e:
                invalid_record(hash_key, e)

        # Pass 3: Mark all specs concrete.  Specs representing real
        # installations must be explicitly marked.
        # We do this *after* all dependencies are connected because if we
        # do it *while* we're constructing specs,it causes hashes to be
        # cached prematurely.
        for hash_key, rec in data.items():
            rec.spec._mark_concrete()

        self._data = data

    def reindex(self, directory_layout):
        """Build database index from scratch based from a directory layout.

        Locks the DB if it isn't locked already.

        """
        # Special transaction to avoid recursive reindex calls and to
        # ignore errors if we need to rebuild a corrupt database.
        def _read_suppress_error():
            try:
                if os.path.isfile(self._index_path):
                    self._read_from_yaml(self._index_path)
            except CorruptDatabaseError as e:
                self._error = e
                self._data = {}

        transaction = WriteTransaction(
            self.lock, _read_suppress_error, self._write, _db_lock_timeout)

        with transaction:
            if self._error:
                tty.warn(
                    "Spack database was corrupt. Will rebuild. Error was:",
                    str(self._error))
                self._error = None

            old_data = self._data
            try:
                self._data = {}

                # Ask the directory layout to traverse the filesystem.
                for spec in directory_layout.all_specs():
                    # Create a spec for each known package and add it.
                    path = directory_layout.path_for_spec(spec)

                    # Try to recover explicit value from old DB, but
                    # default it to False if DB was corrupt.
                    explicit = False
                    if old_data is not None:
                        old_info = old_data.get(spec.dag_hash())
                        if old_info is not None:
                            explicit = old_info.explicit

                    self._add(spec, path, directory_layout, explicit=explicit)

                self._check_ref_counts()

            except:
                # If anything explodes, restore old data, skip write.
                self._data = old_data
                raise

    def _check_ref_counts(self):
        """Ensure consistency of reference counts in the DB.

        Raise an AssertionError if something is amiss.

        Does no locking.
        """
        counts = {}
        for key, rec in self._data.items():
            counts.setdefault(key, 0)
            # XXX(deptype): This checks all dependencies, but build
            #               dependencies might be able to be dropped in the
            #               future.
            for dep in rec.spec.dependencies():
                dep_key = dep.dag_hash()
                counts.setdefault(dep_key, 0)
                counts[dep_key] += 1

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
                self._write_to_yaml(f)
            os.rename(temp_file, self._index_path)
        except:
            # Clean up temp file if something goes wrong.
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise

    def _read(self):
        """Re-read Database from the data in the set location.

        This does no locking.
        """
        if os.path.isfile(self._index_path):
            # Read from YAML file if a database exists
            self._read_from_yaml(self._index_path)

        else:
            # The file doesn't exist, try to traverse the directory.
            # reindex() takes its own write lock, so no lock here.
            self.reindex(spack.install_layout)

    def _add(self, spec, path, directory_layout=None, explicit=False):
        """Add an install record for spec at path to the database.

        This assumes that the spec is not already installed. It
        updates the ref counts on dependencies of the spec in the DB.

        This operation is in-memory, and does not lock the DB.

        """
        key = spec.dag_hash()
        if key in self._data:
            rec = self._data[key]
            rec.installed = True

            # TODO: this overwrites a previous install path (when path !=
            # self._data[key].path), and the old path still has a
            # dependent in the DB. We could consider re-RPATH-ing the
            # dependents.  This case is probably infrequent and may not be
            # worth fixing, but this is where we can discover it.
            rec.path = path

        else:
            self._data[key] = InstallRecord(spec, path, True,
                                            explicit=explicit)
            for dep in spec.dependencies(('link', 'run')):
                self._increment_ref_count(dep, directory_layout)

    def _increment_ref_count(self, spec, directory_layout=None):
        """Recursively examine dependencies and update their DB entries."""
        key = spec.dag_hash()
        if key not in self._data:
            installed = False
            path = None
            if directory_layout:
                path = directory_layout.path_for_spec(spec)
                installed = os.path.isdir(path)

            self._data[key] = InstallRecord(spec.copy(), path, installed)

            for dep in spec.dependencies(('link', 'run')):
                self._increment_ref_count(dep)

        self._data[key].ref_count += 1

    @_autospec
    def add(self, spec, path, explicit=False):
        """Add spec at path to database, locking and reading DB to sync.

        ``add()`` will lock and read from the DB on disk.

        """
        # TODO: ensure that spec is concrete?
        # Entire add is transactional.
        with self.write_transaction():
            self._add(spec, path, explicit=explicit)

    def _get_matching_spec_key(self, spec, **kwargs):
        """Get the exact spec OR get a single spec that matches."""
        key = spec.dag_hash()
        if key not in self._data:
            match = self.query_one(spec, **kwargs)
            if match:
                return match.dag_hash()
            raise KeyError("No such spec in database! %s" % spec)
        return key

    @_autospec
    def get_record(self, spec, **kwargs):
        key = self._get_matching_spec_key(spec, **kwargs)
        return self._data[key]

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
            for dep in spec.dependencies('link'):
                self._decrement_ref_count(dep)

    def _remove(self, spec):
        """Non-locking version of remove(); does real work.
        """
        key = self._get_matching_spec_key(spec)
        rec = self._data[key]

        if rec.ref_count > 0:
            rec.installed = False
            return rec.spec

        del self._data[key]
        for dep in rec.spec.dependencies('link'):
            self._decrement_ref_count(dep)

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

    @_autospec
    def installed_extensions_for(self, extendee_spec):
        """
        Return the specs of all packages that extend
        the given spec
        """
        for s in self.query():
            try:
                if s.package.extends(extendee_spec):
                    yield s.package
            except UnknownPackageError:
                continue
            # skips unknown packages
            # TODO: conditional way to do this instead of catching exceptions

    def query(self, query_spec=any, known=any, installed=True, explicit=any):
        """Run a query on the database.

        ``query_spec``
            Queries iterate through specs in the database and return
            those that satisfy the supplied ``query_spec``.  If
            query_spec is `any`, This will match all specs in the
            database.  If it is a spec, we'll evaluate
            ``spec.satisfies(query_spec)``.

        The query can be constrained by two additional attributes:

        ``known``
            Possible values: True, False, any

            Specs that are "known" are those for which Spack can
            locate a ``package.py`` file -- i.e., Spack "knows" how to
            install them.  Specs that are unknown may represent
            packages that existed in a previous version of Spack, but
            have since either changed their name or been removed.

        ``installed``
            Possible values: True, False, any

            Specs for which a prefix exists are "installed". A spec
            that is NOT installed will be in the database if some
            other spec depends on it but its installation has gone
            away since Spack installed it.

        TODO: Specs are a lot like queries.  Should there be a
              wildcard spec object, and should specs have attributes
              like installed and known that can be queried?  Or are
              these really special cases that only belong here?

        """
        with self.read_transaction():
            results = []
            for key, rec in self._data.items():
                if installed is not any and rec.installed != installed:
                    continue
                if explicit is not any and rec.explicit != explicit:
                    continue
                if known is not any and spack.repo.exists(
                        rec.spec.name) != known:
                    continue
                if query_spec is any or rec.spec.satisfies(query_spec):
                    results.append(rec.spec)

            return sorted(results)

    def query_one(self, query_spec, known=any, installed=True):
        """Query for exactly one spec that matches the query spec.

        Raises an assertion error if more than one spec matches the
        query. Returns None if no installed package matches.

        """
        concrete_specs = self.query(query_spec, known, installed)
        assert len(concrete_specs) <= 1
        return concrete_specs[0] if concrete_specs else None

    def missing(self, spec):
        with self.read_transaction():
            key = spec.dag_hash()
            return key in self._data and not self._data[key].installed


class CorruptDatabaseError(SpackError):
    """Raised when errors are found while reading the database."""


class InvalidDatabaseVersionError(SpackError):

    def __init__(self, expected, found):
        super(InvalidDatabaseVersionError, self).__init__(
            "Expected database version %s but found version %s."
            % (expected, found),
            "`spack reindex` may fix this, or you may need a newer "
            "Spack version.")
