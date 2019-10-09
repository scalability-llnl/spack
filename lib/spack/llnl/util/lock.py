# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import fcntl
import errno
import time
import socket

import llnl.util.tty as tty


__all__ = ['Lock', 'LockTransaction', 'WriteTransaction', 'ReadTransaction',
           'LockError', 'LockTimeoutError',
           'LockPermissionError', 'LockROFileError', 'CantCreateLockError']


class Lock(object):
    """This is an implementation of a filesystem lock using Python's lockf.

    In Python, ``lockf`` actually calls ``fcntl``, so this should work with
    any filesystem implementation that supports locking through the fcntl
    calls.  This includes distributed filesystems like Lustre (when flock
    is enabled) and recent NFS versions.

    Note that this is for managing contention over resources *between*
    processes and not for managing contention between threads in a process: the
    functions of this object are not thread-safe. A process also must not
    maintain multiple locks on the same file.
    """

    def __init__(self, path, start=0, length=0, debug=False,
                 default_timeout=None, desc=''):
        """Construct a new lock on the file at ``path``.

        By default, the lock applies to the whole file.  Optionally,
        caller can specify a byte range beginning ``start`` bytes from
        the start of the file and extending ``length`` bytes from there.

        This exposes a subset of fcntl locking functionality.  It does
        not currently expose the ``whence`` parameter -- ``whence`` is
        always ``os.SEEK_SET`` and ``start`` is always evaluated from the
        beginning of the file.
        """
        self.path = path
        self._file = None
        self._reads = 0
        self._writes = 0

        # byte range parameters
        self._start = start
        self._length = length

        # enable debug mode
        self.debug = debug

        # optional debug description
        self.desc = ' ({0})'.format(desc) if desc else ''

        # If the user doesn't set a default timeout, or if they choose
        # None, 0, etc. then lock attempts will not time out (unless the
        # user sets a timeout for each attempt)
        self.default_timeout = default_timeout or None

        # PID and host of lock holder (only used in debug mode)
        self.pid = self.old_pid = None
        self.host = self.old_host = None

    @staticmethod
    def _poll_interval_generator(_wait_times=None):
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

    def _lock(self, op, timeout=None):
        """This takes a lock using POSIX locks (``fcntl.lockf``).

        The lock is implemented as a spin lock using a nonblocking call
        to ``lockf()``.

        On acquiring an exclusive lock, the lock writes this process's
        pid and host to the lock file, in case the holding process needs
        to be killed later.

        If the lock times out, it raises a ``LockError``. If the lock is
        successfully acquired, the total wait time and the number of attempts
        is returned.
        """
        assert op in (fcntl.LOCK_SH, fcntl.LOCK_EX)
        lock_type = {fcntl.LOCK_SH: 'read', fcntl.LOCK_EX: 'write'}

        timeout = timeout or self.default_timeout

        # Create file and parent directories if they don't exist.
        if self._file is None:
            parent = self._ensure_parent_directory()

            # Open writable files as 'r+' so we can upgrade to write later
            os_mode, fd_mode = (os.O_RDWR | os.O_CREAT), 'r+'
            if os.path.exists(self.path):
                if not os.access(self.path, os.W_OK):
                    if op == fcntl.LOCK_SH:
                        # can still lock read-only files if we open 'r'
                        os_mode, fd_mode = os.O_RDONLY, 'r'
                    else:
                        raise LockROFileError(self.path)

            elif not os.access(parent, os.W_OK):
                raise CantCreateLockError(self.path)

            fd = os.open(self.path, os_mode)
            self._file = os.fdopen(fd, fd_mode)

        elif op == fcntl.LOCK_EX and self._file.mode == 'r':
            # Attempt to upgrade to write lock w/a read-only file.
            # If the file were writable, we'd have opened it 'r+'
            raise LockROFileError(self.path)

        # TODO/TBD: Should max attempts be used?  Configurable?
        max_attempts = timeout * 10 if timeout else 100
        pid = self.pid if self.pid is not None else os.getpid()
        self._debug("PID {0} locking: timeout {1} sec, {2} max attempts".
                    format(pid, timeout, max_attempts))

        poll_intervals = iter(Lock._poll_interval_generator())
        start_time = time.time()
        num_attempts = 0
        while num_attempts < max_attempts:
            if timeout and (time.time() - start_time) >= timeout:
                raise LockTimeoutError("PID {0} timed out waiting for lock.".
                                       format(pid))

            num_attempts += 1
            self._debug("PID {0} attempt #{1}: attempting a {2} lock".
                        format(pid, num_attempts, lock_type[op]))
            if self._poll_lock(op):
                total_wait_time = time.time() - start_time
                return total_wait_time, num_attempts

            time.sleep(next(poll_intervals))

        raise LockLimitError(
            "PID {0} exceeded attempts limit ({1}) waiting for lock.".
            format(pid, max_attempts))

    def _poll_lock(self, op):
        """Attempt to acquire the lock in a non-blocking manner. Return whether
        the locking attempt succeeds
        """
        try:
            # Try to get the lock (will raise if not available.)
            fcntl.lockf(self._file, op | fcntl.LOCK_NB,
                        self._length, self._start, os.SEEK_SET)

            # help for debugging distributed locking
            if self.debug:
                # All locks read the owner PID and host
                self._read_debug_data()

                # Exclusive locks write their PID/host
                if op == fcntl.LOCK_EX:
                    self._write_debug_data()

            return True

        except IOError as e:
            if e.errno == errno.EAGAIN:
                # locked by another process, try again
                pass
            elif e.errno == errno.EACCES:
                # permission denied
                tty.warn("Unable to acquire the lock: {0}".format(str(e)))
            else:
                raise

        return False

    def _ensure_parent_directory(self):
        parent = os.path.dirname(self.path)

        # relative paths to lockfiles in the current directory have no parent
        if not parent:
            return '.'

        try:
            os.makedirs(parent)
        except OSError as e:
            # makedirs can fail when diretory already exists.
            if not (e.errno == errno.EEXIST and os.path.isdir(parent) or
                    e.errno == errno.EISDIR):
                raise
        return parent

    def _read_debug_data(self):
        """Read PID and host data out of the file if it is there."""
        self.old_pid = self.pid
        self.old_host = self.host

        line = self._file.read()
        if line:
            pid, host = line.strip().split(',')
            _, _, self.pid = pid.rpartition('=')
            _, _, self.host = host.rpartition('=')
            self.pid = int(self.pid)

    def _write_debug_data(self):
        """Write PID and host data to the file, recording old values."""
        self.old_pid = self.pid
        self.old_host = self.host

        self.pid = os.getpid()
        self.host = socket.getfqdn()

        # write pid, host to disk to sync over FS
        self._file.seek(0)
        self._file.write("pid=%s,host=%s" % (self.pid, self.host))
        self._file.truncate()
        self._file.flush()
        os.fsync(self._file.fileno())

    def _unlock(self):
        """Releases a lock using POSIX locks (``fcntl.lockf``)

        Releases the lock regardless of mode. Note that read locks may
        be masquerading as write locks, but this removes either.

        """
        fcntl.lockf(self._file, fcntl.LOCK_UN,
                    self._length, self._start, os.SEEK_SET)
        self._file.close()
        self._file = None
        self._reads = 0
        self._writes = 0

    def acquire_read(self, timeout=None):
        """Acquires a recursive, shared lock for reading.

        Read and write locks can be acquired and released in arbitrary
        order, but the POSIX lock is held until all local read and
        write locks are released.

        Returns True if it is the first acquire and actually acquires
        the POSIX lock, False if it is a nested transaction.

        """
        timeout = timeout or self.default_timeout

        lock_type = 'READ LOCK'
        # self._acquiring_debug(lock_type)
        if self._reads == 0 and self._writes == 0:
            self._acquiring_debug(lock_type)
            # can raise LockError.
            wait_time, nattempts = self._lock(fcntl.LOCK_SH, timeout=timeout)
            self._reads += 1
            self._acquired_debug(lock_type, wait_time, nattempts)
            return True
        else:
            # TODO/TBD: Still increment reads if have a write lock?
            #  (See masquerading comment.)
            self._reads += 1
            return False

    def acquire_write(self, timeout=None):
        """Acquires a recursive, exclusive lock for writing.

        Read and write locks can be acquired and released in arbitrary
        order, but the POSIX lock is held until all local read and
        write locks are released.

        Returns True if it is the first acquire and actually acquires
        the POSIX lock, False if it is a nested transaction.

        """
        timeout = timeout or self.default_timeout

        lock_type = 'WRITE LOCK'
        # self._acquiring_debug(lock_type)
        if self._writes == 0:
            self._acquiring_debug(lock_type)
            # can raise LockError.
            wait_time, nattempts = self._lock(fcntl.LOCK_EX, timeout=timeout)
            self._writes += 1
            self._acquired_debug(lock_type, wait_time, nattempts)
            return True
        else:
            # TODO/TBD: Still increment writes if have a write lock?
            #  (See masquerading comment.)
            self._writes += 1
            return False

    def release_read(self):
        """Releases a read lock.

        Returns True if the last recursive lock was released, False if
        there are still outstanding locks.

        Does limited correctness checking: if a read lock is released
        when none are held, this will raise an assertion error.

        """
        assert self._reads > 0

        lock_type = 'READ LOCK'
        # self._releasing_debug(lock_type)
        if self._reads == 1 and self._writes == 0:
            self._releasing_debug(lock_type)
            self._unlock()      # can raise LockError.
            self._released_debug(lock_type)
            return True
        elif self._reads >= 1:
            self._reads -= 1
            return False
        else:
            self._unreleased_warning(lock_type)
            return False

    def release_write(self):
        """Releases a write lock.

        Returns True if the last recursive lock was released, False if
        there are still outstanding locks.

        Does limited correctness checking: if a read lock is released
        when none are held, this will generate a warning.

        """
        assert self._writes > 0

        lock_type = 'WRITE LOCK'
        # self._releasing_debug(lock_type)
        if self._writes == 1 and self._reads == 0:
            self._releasing_debug(lock_type)
            self._unlock()      # can raise LockError.
            self._released_debug(lock_type)
            return True
        elif self._writes >= 1:
            self._writes -= 1
            return False
        else:
            self._unreleased_warning(lock_type)
            return False

    def _debug(self, *args):
        tty.debug(*args)

    def _acquiring_debug(self, lock_type):
        self._debug(self._status_msg(lock_type, 'Acquiring'))

    def _acquired_debug(self, lock_type, wait_time, nattempts):
        attempts_format = 'attempt' if nattempts == 1 else 'attempts'
        if nattempts > 1:
            acquired_attempts_format = ' after {0:0.2f}s and {1:d} {2}'.format(
                wait_time, nattempts, attempts_format)
        else:
            # Dont print anything if we succeeded immediately
            acquired_attempts_format = ''
        self._debug(self._status_msg(lock_type, 'Acquired{0}'.
                                     format(acquired_attempts_format)))

    def _get_counts_desc(self):
        return 'reads {0}, writes {1}'.format(self._reads, self._writes)

    def _released_debug(self, lock_type):
        self._debug(self._status_msg(lock_type, 'Released'))

    def _releasing_debug(self, lock_type):
        self._debug(self._status_msg(lock_type, 'Releasing'))

    def _status_msg(self, lock_type, status):
        status_desc = '[{0}] ({1})'.format(status, self._get_counts_desc())
        return '{0}{1.desc}: {1.path}[{1._start}:{1._length}] {2}'.format(
            lock_type, self, status_desc)

    def _unreleased_warning(self, lock_type):
        tty.warn(self._status_msg(lock_type, 'No lock to release'))


class LockTransaction(object):
    """Simple nested transaction context manager that uses a file lock.

    This class can trigger actions when the lock is acquired for the
    first time and released for the last.

    If the ``acquire_fn`` returns a value, it is used as the return value for
    ``__enter__``, allowing it to be passed as the ``as`` argument of a
    ``with`` statement.

    If ``acquire_fn`` returns a context manager, *its* ``__enter__`` function
    will be called in ``__enter__`` after ``acquire_fn``, and its ``__exit__``
    funciton will be called before ``release_fn`` in ``__exit__``, allowing you
    to nest a context manager to be used along with the lock.

    Timeout for lock is customizable.

    """

    def __init__(self, lock, acquire_fn=None, release_fn=None,
                 timeout=None):
        self._lock = lock
        self._timeout = timeout
        self._acquire_fn = acquire_fn
        self._release_fn = release_fn
        self._as = None

    def __enter__(self):
        if self._enter() and self._acquire_fn:
            self._as = self._acquire_fn()
            if hasattr(self._as, '__enter__'):
                return self._as.__enter__()
            else:
                return self._as

    def __exit__(self, type, value, traceback):
        suppress = False
        if self._exit():
            if self._as and hasattr(self._as, '__exit__'):
                if self._as.__exit__(type, value, traceback):
                    suppress = True
            if self._release_fn:
                if self._release_fn(type, value, traceback):
                    suppress = True
        return suppress


class ReadTransaction(LockTransaction):
    """LockTransaction context manager that does a read and releases it."""
    def _enter(self):
        return self._lock.acquire_read(self._timeout)

    def _exit(self):
        return self._lock.release_read()


class WriteTransaction(LockTransaction):
    """LockTransaction context manager that does a write and releases it."""
    def _enter(self):
        return self._lock.acquire_write(self._timeout)

    def _exit(self):
        return self._lock.release_write()


class LockError(Exception):
    """Raised for any errors related to locks."""


class LockLimitError(LockError):
    """Raised when exceed maximum attempts to acquire a lock."""


class LockTimeoutError(LockError):
    """Raised when an attempt to acquire a lock times out."""


class LockPermissionError(LockError):
    """Raised when there are permission issues with a lock."""


class LockROFileError(LockPermissionError):
    """Tried to take an exclusive lock on a read-only file."""
    def __init__(self, path):
        msg = "Can't take write lock on read-only file: %s" % path
        super(LockROFileError, self).__init__(msg)


class CantCreateLockError(LockPermissionError):
    """Attempt to create a lock in an unwritable location."""
    def __init__(self, path):
        msg = "cannot create lock '%s': " % path
        msg += "file does not exist and location is not writable"
        super(LockError, self).__init__(msg)
