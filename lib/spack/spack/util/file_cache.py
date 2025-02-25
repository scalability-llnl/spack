# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import math
import os
import pathlib
import shutil
from typing import IO, Optional, Tuple, Union

from llnl.util.filesystem import mkdirp, rename

from spack.error import SpackError
from spack.util.lock import Lock, ReadTransaction, WriteTransaction


def _maybe_open(path: Union[str, pathlib.Path]) -> Optional[IO[str]]:
    try:
        return open(path, "r", encoding="utf-8")
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
        return None


class ReadContextManager:
    def __init__(self, path: Union[str, pathlib.Path]) -> None:
        self.path = path

    def __enter__(self) -> Optional[IO[str]]:
        """Return a file object for the cache if it exists."""
        self.cache_file = _maybe_open(self.path)
        return self.cache_file

    def __exit__(self, type, value, traceback):
        if self.cache_file:
            self.cache_file.close()


class WriteContextManager:
    def __init__(self, path: str) -> None:
        self.path = path
        self.tmp_path = f"{self.path}.tmp"

    def __enter__(self) -> Tuple[Optional[IO[str]], IO[str]]:
        """Return (old_file, new_file) file objects, where old_file is optional."""
        self.old_file = _maybe_open(self.path)
        self.new_file = open(self.tmp_path, "w", encoding="utf-8")
        return self.old_file, self.new_file

    def __exit__(self, type, value, traceback):
        if self.old_file:
            self.old_file.close()
        self.new_file.close()

        if value:
            os.remove(self.tmp_path)
        else:
            rename(self.tmp_path, self.path)


class FileCache:
    """This class manages cached data in the filesystem.

    - Cache files are fetched and stored by unique keys.  Keys can be relative
      paths, so that there can be some hierarchy in the cache.

    - The FileCache handles locking cache files for reading and writing, so
      client code need not manage locks for cache entries.

    """

    def __init__(self, root: Union[str, pathlib.Path], timeout=120):
        """Create a file cache object.

        This will create the cache directory if it does not exist yet.

        Args:
            root: specifies the root directory where the cache stores files

            timeout: when there is contention among multiple Spack processes
                for cache files, this specifies how long Spack should wait
                before assuming that there is a deadlock.
        """
        if isinstance(root, str):
            root = pathlib.Path(root)
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

        self._locks = {}
        self.lock_timeout = timeout

    def destroy(self):
        """Remove all files under the cache root."""
        for f in self.root.iterdir():
            if f.is_dir():
                shutil.rmtree(f, True)
            else:
                f.unlink()

    def cache_path(self, key) -> pathlib.Path:
        """Path to the file in the cache for a particular key."""
        return self.root / key

    def _lock_path(self, key) -> pathlib.Path:
        """Path to the file in the cache for a particular key."""
        keyfile = os.path.basename(key)
        keydir = os.path.dirname(key)

        return self.root / keydir / "." + keyfile + ".lock"

    def _get_lock(self, key, start:int=0, length:int=0, timeout:int=0):
        """Create a lock for a key, if necessary, and return a lock object."""
        if not timeout:
            timeout = self.lock_timeout
        _cache_key = key + "-" + str(start) + "-" + str(length)
        if _cache_key not in self._locks:
            self._locks[_cache_key] = Lock(str(self._lock_path(key)), start=start, length=length, default_timeout=timeout)
        return self._locks[_cache_key]

    def init_entry(self, key, start:int=0, length:int=0):
        """Ensure we can access a cache file. Create a lock for it if needed.

        Return whether the cache file exists yet or not.
        """
        cache_path = self.cache_path(key)

        exists = cache_path.exists()
        if exists:
            if not cache_path.is_file():
                raise CacheError("Cache file is not a file: %s" % cache_path)

            if not os.access(cache_path, os.R_OK):
                raise CacheError("Cannot access cache file: %s" % cache_path)
        else:
            # if the file is hierarchical, make parent directories
            parent = cache_path.parent
            if parent != self.root:
                parent.mkdir(parents=True, exist_ok=True)

            if not os.access(parent, os.R_OK | os.W_OK):
                raise CacheError("Cannot access cache directory: %s" % parent)

            # ensure lock is created for this key
            self._get_lock(key, start=start, length=length)
        return exists

    def read_transaction(self, key, start:int=0, length:int=0, timeout:int=0):
        """Get a read transaction on a file cache item.

        Returns a ReadTransaction context manager and opens the cache file for
        reading.  You can use it like this:

           with file_cache_object.read_transaction(key) as cache_file:
               cache_file.read()

        """
        path = self.cache_path(key)
        return ReadTransaction(self._get_lock(key, start=start, length=length, timeout=timeout), acquire=lambda: ReadContextManager(path))

    def write_transaction(self, key, start:int=0, length:int=0, timeout:int=0):
        """Get a write transaction on a file cache item.

        Returns a WriteTransaction context manager that opens a temporary file
        for writing.  Once the context manager finishes, if nothing went wrong,
        moves the file into place on top of the old file atomically.

        """
        path = self.cache_path(key)
        if os.path.exists(path) and not os.access(path, os.W_OK):
            raise CacheError(f"Insufficient permissions to write to file cache at {path}")

        return WriteTransaction(self._get_lock(key, start=start, length=length, timeout=timeout), acquire=lambda: WriteContextManager(path))

    def mtime(self, key) -> float:
        """Return modification time of cache file, or -inf if it does not exist.

        Time is in units returned by os.stat in the mtime field, which is
        platform-dependent.

        """
        if not self.init_entry(key):
            return -math.inf
        else:
            return self.cache_path(key).stat().st_mtime

    def remove(self, key, start:int=0, length:int=0):
        file = self.cache_path(key)
        lock = self._get_lock(key, start=start, length=length)
        try:
            lock.acquire_write()
            file.unlink()
        except OSError as e:
            # File not found is OK, so remove is idempotent.
            if e.errno != errno.ENOENT:
                raise
        finally:
            lock.release_write()


class CacheError(SpackError):
    pass
