# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import fcntl
import errno
import time
import socket
from datetime import datetime

import llnl.util.tty as tty
import spack.util.string


__all__ = ['Lock', 'LockTransaction', 'WriteTransaction', 'ReadTransaction',
           'LockError', 'LockTimeoutError',
           'LockPermissionError', 'LockROFileError', 'CantCreateLockError']

#: Mapping of supported locks to description
lock_type = {fcntl.LOCK_SH: 'read', fcntl.LOCK_EX: 'write'}

#: A useful replacement for functions that should return True when not provided
#: for example.
true_fn = lambda: True


def _attempts_str(wait_time, nattempts):
    # Don't print anything if we succeeded on the first try
    if nattempts <= 1:
        return ''

    attempts = spack.util.string.plural(nattempts, 'attempt')
    return ' after {0:0.2f}s and {1}'.format(wait_time, attempts)


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

    def __init__(self, path, start=0, length=0, default_timeout=None,
                 debug=False, desc=''):
        """Construct a new lock on the file at ``path``.

        By default, the lock applies to the whole file.  Optionally,
        caller can specify a byte range beginning ``start`` bytes from
        the start of the file and extending ``length`` bytes from there.

        This exposes a subset of fcntl locking functionality.  It does
        not currently expose the ``whence`` parameter -- ``whence`` is
        always ``os.SEEK_SET`` and ``start`` is always evaluated from the
        beginning of the file.

        Args:
            path (str): path to the lock
            start (int): optional byte offset at which the lock starts
            length (int): optional number of bytes to lock
            default_timeout (int): number of seconds to wait for lock attempts,
                where None means to wait indefinitely
            debug (bool): debug mode specific to locking
            desc (str): optional debug message lock description, which is
                helpful for distinguishing between different Spack locks.
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

    def __repr__(self):
        """Formal representation of the lock."""
        rep = '{0}('.format(self.__class__.__name__)
        for attr, value in self.__dict__.items():
            rep += '{0}={1}, '.format(attr, value.__repr__())
        return '{0})'.format(rep.strip(', '))

    def __str__(self):
        """Readable string (with key fields) of the lock."""
        location = '{0}[{1}:{2}]'.format(self.path, self._start, self._length)
        timeout = 'timeout={0}'.format(self.default_timeout)
        activity = '#reads={0}, #writes={1}'.format(self._reads, self._writes)
        return '({0}, {1}, {2})'.format(location, timeout, activity)

    def _lock(self, op, timeout=None):
        """This takes a lock using POSIX locks (``fcntl.lockf``).

        The lock is implemented as a spin lock using a nonblocking call
        to ``lockf()``.

        If the lock times out, it raises a ``LockError``. If the lock is
        successfully acquired, the total wait time and the number of attempts
        is returned.
        """
        assert op in lock_type

        self._log_acquiring('{0} LOCK'.format(lock_type[op].upper()))
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

        self._log_debug("{0} locking [{1}:{2}]: timeout {3} sec"
                        .format(lock_type[op], self._start, self._length,
                                timeout))

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

        raise LockTimeoutError("Timed out waiting for a {0} lock."
                               .format(lock_type[op]))

    def _poll_lock(self, op):
        """Attempt to acquire the lock in a non-blocking manner. Return whether
        the locking attempt succeeds
        """
        assert op in lock_type

        try:
            # Try to get the lock (will raise if not available.)
            fcntl.lockf(self._file, op | fcntl.LOCK_NB,
                        self._length, self._start, os.SEEK_SET)

            # help for debugging distributed locking
            if self.debug:
                # All locks read the owner PID and host
                self._read_log_debug_data()
                self._log_debug('{0} locked {1} [{2}:{3}] (owner={4})'
                                .format(lock_type[op], self.path,
                                        self._start, self._length, self.pid))

                # Exclusive locks write their PID/host
                if op == fcntl.LOCK_EX:
                    self._write_log_debug_data()

            return True

        except IOError as e:
            # EAGAIN and EACCES == locked by another process (so try again)
            if e.errno not in (errno.EAGAIN, errno.EACCES):
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

    def _read_log_debug_data(self):
        """Read PID and host data out of the file if it is there."""
        self.old_pid = self.pid
        self.old_host = self.host

        line = self._file.read()
        if line:
            pid, host = line.strip().split(',')
            _, _, self.pid = pid.rpartition('=')
            _, _, self.host = host.rpartition('=')
            self.pid = int(self.pid)

    def _write_log_debug_data(self):
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

        if self._reads == 0 and self._writes == 0:
            # can raise LockError.
            wait_time, nattempts = self._lock(fcntl.LOCK_SH, timeout=timeout)
            self._reads += 1
            # Log if acquired, which includes counts when verbose
            self._log_acquired('READ LOCK', wait_time, nattempts)
            return True
        else:
            # Increment the read count for nested lock tracking
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

        if self._writes == 0:
            # can raise LockError.
            wait_time, nattempts = self._lock(fcntl.LOCK_EX, timeout=timeout)
            self._writes += 1
            # Log if acquired, which includes counts when verbose
            self._log_acquired('WRITE LOCK', wait_time, nattempts)

            # return True only if we weren't nested in a read lock.
            # TODO: we may need to return two values: whether we got
            # the write lock, and whether this is acquiring a read OR
            # write lock for the first time. Now it returns the latter.
            return self._reads == 0
        else:
            # Increment the write count for nested lock tracking
            self._writes += 1
            return False

    def is_write_locked(self):
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

    def downgrade_write_to_read(self, timeout=None):
        """
        Downgrade from an exclusive write lock to a shared read.

        Raises:
            LockDowngradeError: if this is an attempt at a nested transaction
        """
        timeout = timeout or self.default_timeout

        if self._writes == 1 and self._reads == 0:
            self._log_downgrading()
            # can raise LockError.
            wait_time, nattempts = self._lock(fcntl.LOCK_SH, timeout=timeout)
            self._reads = 1
            self._writes = 0
            self._log_downgraded(wait_time, nattempts)
        else:
            raise LockDowngradeError(self.path)

    def upgrade_read_to_write(self, timeout=None):
        """
        Attempts to upgrade from a shared read lock to an exclusive write.

        Raises:
            LockUpgradeError: if this is an attempt at a nested transaction
        """
        timeout = timeout or self.default_timeout

        if self._reads == 1 and self._writes == 0:
            self._log_upgrading()
            # can raise LockError.
            wait_time, nattempts = self._lock(fcntl.LOCK_EX, timeout=timeout)
            self._reads = 0
            self._writes = 1
            self._log_upgraded(wait_time, nattempts)
        else:
            raise LockUpgradeError(self.path)

    def release_read(self, release_fn=None):
        """Releases a read lock.

        Arguments:
            release_fn (callable): function to call *before* the last recursive
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

        locktype = 'READ LOCK'
        if self._reads == 1 and self._writes == 0:
            self._log_releasing(locktype)

            # we need to call release_fn before releasing the lock
            release_fn = release_fn or true_fn
            result = release_fn()

            self._unlock()      # can raise LockError.
            self._reads = 0
            self._log_released(locktype)
            return result
        else:
            self._reads -= 1
            return False

    def release_write(self, release_fn=None):
        """Releases a write lock.

        Arguments:
            release_fn (callable): function to call before the last recursive
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

        locktype = 'WRITE LOCK'
        if self._writes == 1 and self._reads == 0:
            self._log_releasing(locktype)

            # we need to call release_fn before releasing the lock
            result = release_fn()

            self._unlock()      # can raise LockError.
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

    def _get_counts_desc(self):
        return '(reads {0}, writes {1})'.format(self._reads, self._writes) \
            if tty.is_verbose() else ''

    def _log_acquired(self, locktype, wait_time, nattempts):
        attempts_part = _attempts_str(wait_time, nattempts)
        now = datetime.now()
        desc = 'Acquired at %s' % now.strftime("%H:%M:%S.%f")
        self._log_debug(self._status_msg(locktype, '{0}{1}'
                        .format(desc, attempts_part)))

    def _log_acquiring(self, locktype):
        self._log_debug(self._status_msg(locktype, 'Acquiring'), level=3)

    def _log_debug(self, *args, **kwargs):
        """Output lock debug messages."""
        kwargs['level'] = kwargs.get('level', 2)
        tty.debug(*args, **kwargs)

    def _log_downgraded(self, wait_time, nattempts):
        attempts_part = _attempts_str(wait_time, nattempts)
        now = datetime.now()
        desc = 'Downgraded at %s' % now.strftime("%H:%M:%S.%f")
        self._log_debug(self._status_msg('READ LOCK', '{0}{1}'
                        .format(desc, attempts_part)))

    def _log_downgrading(self):
        self._log_debug(self._status_msg('WRITE LOCK', 'Downgrading'), level=3)

    def _log_released(self, locktype):
        now = datetime.now()
        desc = 'Released at %s' % now.strftime("%H:%M:%S.%f")
        self._log_debug(self._status_msg(locktype, desc))

    def _log_releasing(self, locktype):
        self._log_debug(self._status_msg(locktype, 'Releasing'), level=3)

    def _log_upgraded(self, wait_time, nattempts):
        attempts_part = _attempts_str(wait_time, nattempts)
        now = datetime.now()
        desc = 'Upgraded at %s' % now.strftime("%H:%M:%S.%f")
        self._log_debug(self._status_msg('WRITE LOCK', '{0}{1}'.
                        format(desc, attempts_part)))

    def _log_upgrading(self):
        self._log_debug(self._status_msg('READ LOCK', 'Upgrading'), level=3)

    def _status_msg(self, locktype, status):
        status_desc = '[{0}] {1}'.format(status, self._get_counts_desc())
        return '{0}{1.desc}: {1.path}[{1._start}:{1._length}] {2}'.format(
            locktype, self, status_desc)


class LockTransaction(object):
    """Simple nested transaction context manager that uses a file lock.

    Arguments:
        lock (Lock): underlying lock for this transaction to be accquired on
            enter and released on exit
        acquire (callable or contextmanager): function to be called after lock
            is acquired, or contextmanager to enter after acquire and leave
            before release.
        release (callable): function to be called before release. If
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

    def __init__(self, lock, acquire=None, release=None, timeout=None):
        self._lock = lock
        self._timeout = timeout
        self._acquire_fn = acquire
        self._release_fn = release
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

        def release_fn():
            if self._release_fn is not None:
                return self._release_fn(type, value, traceback)

        if self._as and hasattr(self._as, '__exit__'):
            if self._as.__exit__(type, value, traceback):
                suppress = True

        if self._exit(release_fn):
            suppress = True

        return suppress


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
        super(LockDowngradeError, self).__init__(msg)


class LockLimitError(LockError):
    """Raised when exceed maximum attempts to acquire a lock."""


class LockTimeoutError(LockError):
    """Raised when an attempt to acquire a lock times out."""


class LockUpgradeError(LockError):
    """Raised when unable to upgrade from a read to a write lock."""
    def __init__(self, path):
        msg = "Cannot upgrade lock from read to write on file: %s" % path
        super(LockUpgradeError, self).__init__(msg)


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
