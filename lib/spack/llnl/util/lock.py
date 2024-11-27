# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import os
import socket
import sys
import time
from datetime import datetime
from types import TracebackType
from typing import IO, Any, Callable, ContextManager, Dict, Generator, Optional, Tuple, Type, Union

from llnl.util import lang, tty

from ..string import plural

if sys.platform != "win32":
    import fcntl


__all__ = [
    "Lock",
    "LockDowngradeError",
    "LockUpgradeError",
    "LockTransaction",
    "WriteTransaction",
    "ReadTransaction",
    "LockError",
    "LockTimeoutError",
    "LockPermissionError",
    "LockROFileError",
    "CantCreateLockError",
]


ReleaseFnType = Optional[Callable[[], bool]]


def true_fn() -> bool:
    """A function that always returns True."""
    return True


class OpenFile:
    """Record for keeping track of open lockfiles (with reference counting).

    There's really only one ``OpenFile`` per inode, per process, but we record the
    filehandle here as it's the thing we end up using in python code.  You can get
    the file descriptor from the file handle if needed -- or we could make this track
    file descriptors as well in the future.
    """

    def __init__(self, fh: IO) -> None:
        self.fh = fh
        self.refs = 0


class OpenFileTracker:
    """Track open lockfiles, to minimize number of open file descriptors.

    The ``fcntl`` locks that Spack uses are associated with an inode and a process.
    This is convenient, because if a process exits, it releases its locks.
    Unfortunately, this also means that if you close a file, *all* locks associated
    with that file's inode are released, regardless of whether the process has any
    other open file descriptors on it.

    Because of this, we need to track open lock files so that we only close them when
    a process no longer needs them.  We do this by tracking each lockfile by its
    inode and process id.  This has several nice properties:

    1. Tracking by pid ensures that, if we fork, we don't inadvertently track the parent
       process's lockfiles. ``fcntl`` locks are not inherited across forks, so we'll
       just track new lockfiles in the child.
    2. Tracking by inode ensures that referencs are counted per inode, and that we don't
       inadvertently close a file whose inode still has open locks.
    3. Tracking by both pid and inode ensures that we only open lockfiles the minimum
       number of times necessary for the locks we have.

    Note: as mentioned elsewhere, these locks aren't thread safe -- they're designed to
    work in Python and assume the GIL.
    """

    def __init__(self) -> None:
        """Create a new ``OpenFileTracker``."""
        self._descriptors: Dict[Any, OpenFile] = {}

    def get_fh(self, path: str) -> IO:
        """Get a filehandle for a lockfile.

        This routine will open writable files for read/write even if you're asking
        for a shared (read-only) lock. This is so that we can upgrade to an exclusive
        (write) lock later if requested.

        Arguments:
          path: path to lock file we want a filehandle for
        """
        # Open writable files as 'r+' so we can upgrade to write later
        os_mode, fh_mode = (os.O_RDWR | os.O_CREAT), "r+"

        pid = os.getpid()
        open_file = None  # OpenFile object, if there is one
        stat = None  # stat result for the lockfile, if it exists

        try:
            # see whether we've seen this inode/pid before
            stat = os.stat(path)
            key = (stat.st_dev, stat.st_ino, pid)
            open_file = self._descriptors.get(key)

        except OSError as e:
            if e.errno != errno.ENOENT:  # only handle file not found
                raise

            # path does not exist -- fail if we won't be able to create it
            parent = os.path.dirname(path) or "."
            if not os.access(parent, os.W_OK):
                raise CantCreateLockError(path)

        # if there was no already open file, we'll need to open one
        if not open_file:
            if stat and not os.access(path, os.W_OK):
                # we know path exists but not if it's writable. If it's read-only,
                # only open the file for reading (and fail if we're trying to get
                # an exclusive (write) lock on it)
                os_mode, fh_mode = os.O_RDONLY, "r"

            fd = os.open(path, os_mode)
            fh = os.fdopen(fd, fh_mode)
            open_file = OpenFile(fh)

            # if we just created the file, we'll need to get its inode here
            if not stat:
                stat = os.fstat(fd)
                key = (stat.st_dev, stat.st_ino, pid)

            self._descriptors[key] = open_file

        open_file.refs += 1
        return open_file.fh

    def release_by_stat(self, stat):
        key = (stat.st_dev, stat.st_ino, os.getpid())
        open_file = self._descriptors.get(key)
        assert open_file, "Attempted to close non-existing inode: %s" % stat.st_ino

        open_file.refs -= 1
        if not open_file.refs:
            del self._descriptors[key]
            open_file.fh.close()

    def release_by_fh(self, fh):
        self.release_by_stat(os.fstat(fh.fileno()))

    def purge(self):
        for key in list(self._descriptors.keys()):
            self._descriptors[key].fh.close()
            del self._descriptors[key]


#: Open file descriptors for locks in this process. Used to prevent one process
#: from opening the sam file many times for different byte range locks
FILE_TRACKER = OpenFileTracker()


def _attempts_str(wait_time, nattempts):
    # Don't print anything if we succeeded on the first try
    if nattempts <= 1:
        return ""

    attempts = plural(nattempts, "attempt")
    return " after {} and {}".format(lang.pretty_seconds(wait_time), attempts)


class LockType:
    READ = 0
    WRITE = 1

    @staticmethod
    def to_str(tid):
        ret = "READ"
        if tid == LockType.WRITE:
            ret = "WRITE"
        return ret

    @staticmethod
    def to_module(tid):
        lock = fcntl.LOCK_SH
        if tid == LockType.WRITE:
            lock = fcntl.LOCK_EX
        return lock

    @staticmethod
    def is_valid(op: int) -> bool:
        return op == LockType.READ or op == LockType.WRITE


class Lock:
    """This is an implementation of a filesystem lock using Python's lockf.

    In Python, ``lockf`` actually calls ``fcntl``, so this should work with
    any filesystem implementation that supports locking through the fcntl
    calls.  This includes distributed filesystems like Lustre (when flock
    is enabled) and recent NFS versions.

    Note that this is for managing contention over resources *between*
    processes and not for managing contention between threads in a process: the
    functions of this object are not thread-safe. A process also must not
    maintain multiple locks on the same file (or, more specifically, on
    overlapping byte ranges in the same file).
    """

    def __init__(
        self,
        path: str,
        *,
        start: int = 0,
        length: int = 0,
        default_timeout: Optional[float] = None,
        debug: bool = False,
        desc: str = "",
    ) -> None:
        """Construct a new lock on the file at ``path``.

        By default, the lock applies to the whole file.  Optionally,
        caller can specify a byte range beginning ``start`` bytes from
        the start of the file and extending ``length`` bytes from there.

        This exposes a subset of fcntl locking functionality.  It does
        not currently expose the ``whence`` parameter -- ``whence`` is
        always ``os.SEEK_SET`` and ``start`` is always evaluated from the
        beginning of the file.

        Args:
            path: path to the lock
            start: optional byte offset at which the lock starts
            length: optional number of bytes to lock
            default_timeout: seconds to wait for lock attempts,
                where None means to wait indefinitely
            debug: debug mode specific to locking
            desc: optional debug message lock description, which is
                helpful for distinguishing between different Spack locks.
        """
        self.path = path
        self._file: Optional[IO] = None
        self._reads = 0
        self._writes = 0

        # byte range parameters
        self._start = start
        self._length = length

        # enable debug mode
        self.debug = debug

        # optional debug description
        self.desc = f" ({desc})" if desc else ""

        # If the user doesn't set a default timeout, or if they choose
        # None, 0, etc. then lock attempts will not time out (unless the
        # user sets a timeout for each attempt)
        self.default_timeout = default_timeout or None

        # PID and host of lock holder (only used in debug mode)
        self.pid: Optional[int] = None
        self.old_pid: Optional[int] = None
        self.host: Optional[str] = None
        self.old_host: Optional[str] = None

    @staticmethod
    def _poll_interval_generator(
        _wait_times: Optional[Tuple[float, float, float]] = None
    ) -> Generator[float, None, None]:
        """This implements a backoff scheme for polling a contended resource
        by suggesting a succession of wait times between polls.

        It suggests a poll interval of .1s until 2 seconds have passed,
        then a poll interval of .2s until 10 seconds have passed, and finally
        (for all requests after 10s) suggests a poll interval of .5s.

        This doesn't actually track elapsed time, it estimates the waiting
        time as though the caller always waits for the full length of time
        suggested by this function.
        """
        num_requests = 0
        stage1, stage2, stage3 = _wait_times or (1e-1, 2e-1, 5e-1)
        wait_time = stage1
        while True:
            if num_requests >= 60:  # 40 * .2 = 8
                wait_time = stage3
            elif num_requests >= 20:  # 20 * .1 = 2
                wait_time = stage2
            num_requests += 1
            yield wait_time

    def __repr__(self) -> str:
        """Formal representation of the lock."""
        rep = "{0}(".format(self.__class__.__name__)
        for attr, value in self.__dict__.items():
            rep += "{0}={1}, ".format(attr, value.__repr__())
        return "{0})".format(rep.strip(", "))

    def __str__(self) -> str:
        """Readable string (with key fields) of the lock."""
        location = "{0}[{1}:{2}]".format(self.path, self._start, self._length)
        timeout = "timeout={0}".format(self.default_timeout)
        activity = "#reads={0}, #writes={1}".format(self._reads, self._writes)
        return "({0}, {1}, {2})".format(location, timeout, activity)

    def _lock(self, op: int, timeout: Optional[float] = None) -> Tuple[float, int]:
        """This takes a lock using POSIX locks (``fcntl.lockf``).

        The lock is implemented as a spin lock using a nonblocking call
        to ``lockf()``.

        If the lock times out, it raises a ``LockError``. If the lock is
        successfully acquired, the total wait time and the number of attempts
        is returned.
        """
        assert LockType.is_valid(op)
        op_str = LockType.to_str(op)

        self._log_acquiring("{0} LOCK".format(op_str))
        timeout = timeout or self.default_timeout

        # Create file and parent directories if they don't exist.
        if self._file is None:
            self._ensure_parent_directory()
            self._file = FILE_TRACKER.get_fh(self.path)

        if LockType.to_module(op) == fcntl.LOCK_EX and self._file.mode == "r":
            # Attempt to upgrade to write lock w/a read-only file.
            # If the file were writable, we'd have opened it 'r+'
            raise LockROFileError(self.path)

        self._log_debug(
            "{} locking [{}:{}]: timeout {}".format(
                op_str.lower(), self._start, self._length, lang.pretty_seconds(timeout or 0)
            )
        )

        poll_intervals = iter(Lock._poll_interval_generator())
        start_time = time.time()
        num_attempts = 0
        while (not timeout) or (time.time() - start_time) < timeout:
            num_attempts += 1
            if self._poll_lock(op):
                total_wait_time = time.time() - start_time
                return total_wait_time, num_attempts

            time.sleep(next(poll_intervals))

        # TBD: Is an extra attempt after timeout needed/appropriate?
        num_attempts += 1
        if self._poll_lock(op):
            total_wait_time = time.time() - start_time
            return total_wait_time, num_attempts

        total_wait_time = time.time() - start_time
        raise LockTimeoutError(op_str.lower(), self.path, total_wait_time, num_attempts)

    def _poll_lock(self, op: int) -> bool:
        """Attempt to acquire the lock in a non-blocking manner. Return whether
        the locking attempt succeeds
        """
        assert self._file is not None, "cannot poll a lock without the file being set"
        module_op = LockType.to_module(op)
        try:
            # Try to get the lock (will raise if not available.)
            fcntl.lockf(
                self._file.fileno(),
                module_op | fcntl.LOCK_NB,
                self._length,
                self._start,
                os.SEEK_SET,
            )

            # help for debugging distributed locking
            if self.debug:
                # All locks read the owner PID and host
                self._read_log_debug_data()
                self._log_debug(
                    "{0} locked {1} [{2}:{3}] (owner={4})".format(
                        LockType.to_str(op), self.path, self._start, self._length, self.pid
                    )
                )

                # Exclusive locks write their PID/host
                if module_op == fcntl.LOCK_EX:
                    self._write_log_debug_data()

            return True

        except IOError as e:
            # EAGAIN and EACCES == locked by another process (so try again)
            if e.errno not in (errno.EAGAIN, errno.EACCES):
                raise

        return False

    def _ensure_parent_directory(self) -> str:
        parent = os.path.dirname(self.path)

        # relative paths to lockfiles in the current directory have no parent
        if not parent:
            return "."

        try:
            os.makedirs(parent)
        except OSError as e:
            # os.makedirs can fail in a number of ways when the directory already exists.
            # With EISDIR, we know it exists, and others like EEXIST, EACCES, and EROFS
            # are fine if we ensure that the directory exists.
            # Python 3 allows an exist_ok parameter and ignores any OSError as long as
            # the directory exists.
            if not (e.errno == errno.EISDIR or os.path.isdir(parent)):
                raise
        return parent

    def _read_log_debug_data(self) -> None:
        """Read PID and host data out of the file if it is there."""
        assert self._file is not None, "cannot read debug log without the file being set"
        self.old_pid = self.pid
        self.old_host = self.host

        line = self._file.read()
        if line:
            pid, host = line.strip().split(",")
            _, _, pid = pid.rpartition("=")
            _, _, self.host = host.rpartition("=")
            self.pid = int(pid)

    def _write_log_debug_data(self) -> None:
        """Write PID and host data to the file, recording old values."""
        assert self._file is not None, "cannot write debug log without the file being set"
        self.old_pid = self.pid
        self.old_host = self.host

        self.pid = os.getpid()
        self.host = socket.gethostname()

        # write pid, host to disk to sync over FS
        self._file.seek(0)
        self._file.write("pid=%s,host=%s" % (self.pid, self.host))
        self._file.truncate()
        self._file.flush()
        os.fsync(self._file.fileno())

    def _unlock(self) -> None:
        """Releases a lock using POSIX locks (``fcntl.lockf``)

        Releases the lock regardless of mode. Note that read locks may
        be masquerading as write locks, but this removes either.

        """
        assert self._file is not None, "cannot unlock without the file being set"
        fcntl.lockf(self._file.fileno(), fcntl.LOCK_UN, self._length, self._start, os.SEEK_SET)
        FILE_TRACKER.release_by_fh(self._file)
        self._file = None
        self._reads = 0
        self._writes = 0

    def acquire_read(self, timeout: Optional[float] = None) -> bool:
        """Acquires a recursive, shared lock for reading.

        Read and write locks can be acquired and released in arbitrary
        order, but the POSIX lock is held until all local read and
        write locks are released.

        Returns True if it is the first acquire and actually acquires
        the POSIX lock, False if it is a nested transaction.

        """
        timeout = timeout or self.default_timeout

        if self._reads == 0 and self._writes == 0:
            # can raise LockError.
            wait_time, nattempts = self._lock(LockType.READ, timeout=timeout)
            self._reads += 1
            # Log if acquired, which includes counts when verbose
            self._log_acquired("READ LOCK", wait_time, nattempts)
            return True
        else:
            # Increment the read count for nested lock tracking
            self._reads += 1
            return False

    def acquire_write(self, timeout: Optional[float] = None) -> bool:
        """Acquires a recursive, exclusive lock for writing.

        Read and write locks can be acquired and released in arbitrary
        order, but the POSIX lock is held until all local read and
        write locks are released.

        Returns True if it is the first acquire and actually acquires
        the POSIX lock, False if it is a nested transaction.

        """
        timeout = timeout or self.default_timeout

        if self._writes == 0:
            # can raise LockError.
            wait_time, nattempts = self._lock(LockType.WRITE, timeout=timeout)
            self._writes += 1
            # Log if acquired, which includes counts when verbose
            self._log_acquired("WRITE LOCK", wait_time, nattempts)

            # return True only if we weren't nested in a read lock.
            # TODO: we may need to return two values: whether we got
            # the write lock, and whether this is acquiring a read OR
            # write lock for the first time. Now it returns the latter.
            return self._reads == 0
        else:
            # Increment the write count for nested lock tracking
            self._writes += 1
            return False

    def is_write_locked(self) -> bool:
        """Check if the file is write locked

        Return:
            (bool): ``True`` if the path is write locked, otherwise, ``False``
        """
        try:
            self.acquire_read()

            # If we have a read lock then no other process has a write lock.
            self.release_read()
        except LockTimeoutError:
            # Another process is holding a write lock on the file
            return True

        return False

    def downgrade_write_to_read(self, timeout: Optional[float] = None) -> None:
        """
        Downgrade from an exclusive write lock to a shared read.

        Raises:
            LockDowngradeError: if this is an attempt at a nested transaction
        """
        timeout = timeout or self.default_timeout

        if self._writes == 1 and self._reads == 0:
            self._log_downgrading()
            # can raise LockError.
            wait_time, nattempts = self._lock(LockType.READ, timeout=timeout)
            self._reads = 1
            self._writes = 0
            self._log_downgraded(wait_time, nattempts)
        else:
            raise LockDowngradeError(self.path)

    def upgrade_read_to_write(self, timeout: Optional[float] = None) -> None:
        """
        Attempts to upgrade from a shared read lock to an exclusive write.

        Raises:
            LockUpgradeError: if this is an attempt at a nested transaction
        """
        timeout = timeout or self.default_timeout

        if self._reads == 1 and self._writes == 0:
            self._log_upgrading()
            # can raise LockError.
            wait_time, nattempts = self._lock(LockType.WRITE, timeout=timeout)
            self._reads = 0
            self._writes = 1
            self._log_upgraded(wait_time, nattempts)
        else:
            raise LockUpgradeError(self.path)

    def release_read(self, release_fn: ReleaseFnType = None) -> bool:
        """Releases a read lock.

        Arguments:
            release_fn (typing.Callable): function to call *before* the last recursive
                lock (read or write) is released.

        If the last recursive lock will be released, then this will call
        release_fn and return its result (if provided), or return True
        (if release_fn was not provided).

        Otherwise, we are still nested inside some other lock, so do not
        call the release_fn and, return False.

        Does limited correctness checking: if a read lock is released
        when none are held, this will raise an assertion error.

        """
        assert self._reads > 0

        locktype = "READ LOCK"
        if self._reads == 1 and self._writes == 0:
            self._log_releasing(locktype)

            # we need to call release_fn before releasing the lock
            release_fn = release_fn or true_fn
            result = release_fn()

            self._unlock()  # can raise LockError.
            self._reads = 0
            self._log_released(locktype)
            return result
        else:
            self._reads -= 1
            return False

    def release_write(self, release_fn: ReleaseFnType = None) -> bool:
        """Releases a write lock.

        Arguments:
            release_fn (typing.Callable): function to call before the last recursive
                write is released.

        If the last recursive *write* lock will be released, then this
        will call release_fn and return its result (if provided), or
        return True (if release_fn was not provided). Otherwise, we are
        still nested inside some other write lock, so do not call the
        release_fn, and return False.

        Does limited correctness checking: if a read lock is released
        when none are held, this will raise an assertion error.

        """
        assert self._writes > 0
        release_fn = release_fn or true_fn

        locktype = "WRITE LOCK"
        if self._writes == 1 and self._reads == 0:
            self._log_releasing(locktype)

            # we need to call release_fn before releasing the lock
            result = release_fn()

            self._unlock()  # can raise LockError.
            self._writes = 0
            self._log_released(locktype)
            return result
        else:
            self._writes -= 1

            # when the last *write* is released, we call release_fn here
            # instead of immediately before releasing the lock.
            if self._writes == 0:
                return release_fn()
            else:
                return False

    def cleanup(self) -> None:
        if self._reads == 0 and self._writes == 0:
            os.unlink(self.path)
        else:
            raise LockError("Attempting to cleanup active lock.")

    def _get_counts_desc(self) -> str:
        return (
            "(reads {0}, writes {1})".format(self._reads, self._writes) if tty.is_verbose() else ""
        )

    def _log_acquired(self, locktype, wait_time, nattempts) -> None:
        attempts_part = _attempts_str(wait_time, nattempts)
        now = datetime.now()
        desc = "Acquired at %s" % now.strftime("%H:%M:%S.%f")
        self._log_debug(self._status_msg(locktype, "{0}{1}".format(desc, attempts_part)))

    def _log_acquiring(self, locktype) -> None:
        self._log_debug(self._status_msg(locktype, "Acquiring"), level=3)

    def _log_debug(self, *args, **kwargs) -> None:
        """Output lock debug messages."""
        kwargs["level"] = kwargs.get("level", 2)
        tty.debug(*args, **kwargs)

    def _log_downgraded(self, wait_time, nattempts) -> None:
        attempts_part = _attempts_str(wait_time, nattempts)
        now = datetime.now()
        desc = "Downgraded at %s" % now.strftime("%H:%M:%S.%f")
        self._log_debug(self._status_msg("READ LOCK", "{0}{1}".format(desc, attempts_part)))

    def _log_downgrading(self) -> None:
        self._log_debug(self._status_msg("WRITE LOCK", "Downgrading"), level=3)

    def _log_released(self, locktype) -> None:
        now = datetime.now()
        desc = "Released at %s" % now.strftime("%H:%M:%S.%f")
        self._log_debug(self._status_msg(locktype, desc))

    def _log_releasing(self, locktype) -> None:
        self._log_debug(self._status_msg(locktype, "Releasing"), level=3)

    def _log_upgraded(self, wait_time, nattempts) -> None:
        attempts_part = _attempts_str(wait_time, nattempts)
        now = datetime.now()
        desc = "Upgraded at %s" % now.strftime("%H:%M:%S.%f")
        self._log_debug(self._status_msg("WRITE LOCK", "{0}{1}".format(desc, attempts_part)))

    def _log_upgrading(self) -> None:
        self._log_debug(self._status_msg("READ LOCK", "Upgrading"), level=3)

    def _status_msg(self, locktype: str, status: str) -> str:
        status_desc = "[{0}] {1}".format(status, self._get_counts_desc())
        return "{0}{1.desc}: {1.path}[{1._start}:{1._length}] {2}".format(
            locktype, self, status_desc
        )


class LockTransaction:
    """Simple nested transaction context manager that uses a file lock.

    Arguments:
        lock (Lock): underlying lock for this transaction to be accquired on
            enter and released on exit
        acquire (typing.Callable or contextlib.contextmanager): function to be called
            after lock is acquired, or contextmanager to enter after acquire and leave
            before release.
        release (typing.Callable): function to be called before release. If
            ``acquire`` is a contextmanager, this will be called *after*
            exiting the nexted context and before the lock is released.
        timeout (float): number of seconds to set for the timeout when
            accquiring the lock (default no timeout)

    If the ``acquire_fn`` returns a value, it is used as the return value for
    ``__enter__``, allowing it to be passed as the ``as`` argument of a
    ``with`` statement.

    If ``acquire_fn`` returns a context manager, *its* ``__enter__`` function
    will be called after the lock is acquired, and its ``__exit__`` funciton
    will be called before ``release_fn`` in ``__exit__``, allowing you to
    nest a context manager inside this one.

    Timeout for lock is customizable.

    """

    def __init__(
        self,
        lock: Lock,
        acquire: Union[ReleaseFnType, ContextManager] = None,
        release: Union[ReleaseFnType, ContextManager] = None,
        timeout: Optional[float] = None,
    ) -> None:
        self._lock = lock
        self._timeout = timeout
        self._acquire_fn = acquire
        self._release_fn = release
        self._as = None

    def __enter__(self):
        if self._enter() and self._acquire_fn:
            self._as = self._acquire_fn()
            if hasattr(self._as, "__enter__"):
                return self._as.__enter__()
            else:
                return self._as

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        suppress = False

        def release_fn():
            if self._release_fn is not None:
                return self._release_fn(exc_type, exc_value, traceback)

        if self._as and hasattr(self._as, "__exit__"):
            if self._as.__exit__(exc_type, exc_value, traceback):
                suppress = True

        if self._exit(release_fn):
            suppress = True

        return suppress

    def _enter(self) -> bool:
        return NotImplemented

    def _exit(self, release_fn: ReleaseFnType) -> bool:
        return NotImplemented


class ReadTransaction(LockTransaction):
    """LockTransaction context manager that does a read and releases it."""

    def _enter(self):
        return self._lock.acquire_read(self._timeout)

    def _exit(self, release_fn):
        return self._lock.release_read(release_fn)


class WriteTransaction(LockTransaction):
    """LockTransaction context manager that does a write and releases it."""

    def _enter(self):
        return self._lock.acquire_write(self._timeout)

    def _exit(self, release_fn):
        return self._lock.release_write(release_fn)


class LockError(Exception):
    """Raised for any errors related to locks."""


class LockDowngradeError(LockError):
    """Raised when unable to downgrade from a write to a read lock."""

    def __init__(self, path):
        msg = "Cannot downgrade lock from write to read on file: %s" % path
        super().__init__(msg)


class LockTimeoutError(LockError):
    """Raised when an attempt to acquire a lock times out."""

    def __init__(self, lock_type, path, time, attempts):
        fmt = "Timed out waiting for a {} lock after {}.\n    Made {} {} on file: {}"
        super().__init__(
            fmt.format(
                lock_type,
                lang.pretty_seconds(time),
                attempts,
                "attempt" if attempts == 1 else "attempts",
                path,
            )
        )


class LockUpgradeError(LockError):
    """Raised when unable to upgrade from a read to a write lock."""

    def __init__(self, path):
        msg = "Cannot upgrade lock from read to write on file: %s" % path
        super().__init__(msg)


class LockPermissionError(LockError):
    """Raised when there are permission issues with a lock."""


class LockROFileError(LockPermissionError):
    """Tried to take an exclusive lock on a read-only file."""

    def __init__(self, path):
        msg = "Can't take write lock on read-only file: %s" % path
        super().__init__(msg)


class CantCreateLockError(LockPermissionError):
    """Attempt to create a lock in an unwritable location."""

    def __init__(self, path):
        msg = "cannot create lock '%s': " % path
        msg += "file does not exist and location is not writable"
        super().__init__(msg)
