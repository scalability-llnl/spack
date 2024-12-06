# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""These tests ensure that our lock works correctly.

This can be run in two ways.

First, it can be run as a node-local test, with a typical invocation like
this::

    spack test lock

You can *also* run it as an MPI program, which allows you to test locks
across nodes.  So, e.g., you can run the test like this::

    mpirun -n 7 spack test lock

And it will test locking correctness among MPI processes.  Ideally, you
want the MPI processes to span across multiple nodes, so, e.g., for Slurm
you might do this::

    srun -N 7 -n 7 -m cyclic spack test lock

You can use this to test whether your shared filesystem properly supports
POSIX reader-writer locking with byte ranges through fcntl.

If you want to test on multiple filesystems, you can modify the
``locations`` list below.  By default it looks like this::

    locations = [
        tempfile.gettempdir(),  # standard tmp directory (potentially local)
        '/nfs/tmp2/%u',         # NFS tmp mount
        '/p/lscratch*/%u'       # Lustre scratch mount
    ]

Add names and paths for your preferred filesystem mounts to test on them;
the tests are parametrized to run on all the filesystems listed in this
dict.  Note that 'tmp' will be skipped for MPI testing, as it is often a
node-local filesystem, and multi-node tests will fail if the locks aren't
actually on a shared filesystem.

"""
import collections
import errno
import getpass
import glob
import os
import shutil
import socket
import stat
import sys
import tempfile
import traceback
from contextlib import contextmanager
from multiprocessing import Process, Queue

import pytest

import llnl.util.lock as lk
import llnl.util.multiproc as mp
from llnl.util.filesystem import getuid, touch

if sys.platform != "win32":
    import fcntl

pytestmark = pytest.mark.not_on_windows("does not run on windows")


#
# This test can be run with MPI.  MPI is "enabled" if we can import
# mpi4py and the number of total MPI processes is greater than 1.
# Otherwise it just runs as a node-local test.
#
# NOTE: MPI mode is different from node-local mode in that node-local
# mode will spawn its own test processes, while MPI mode assumes you've
# run this script as a SPMD application.  In MPI mode, no additional
# processes are spawned, and you need to ensure that you mpirun the
# script with enough processes for all the multiproc_test cases below.
#
# If you don't run with enough processes, tests that require more
# processes than you currently have will be skipped.
#
mpi = False
comm = None
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    if comm.size > 1:
        mpi = True
except ImportError:
    pass


"""This is a list of filesystem locations to test locks in.  Paths are
expanded so that %u is replaced with the current username. '~' is also
legal and will be expanded to the user's home directory.

Tests are skipped for directories that don't exist, so you'll need to
update this with the locations of NFS, Lustre, and other mounts on your
system.
"""
locations = [
    tempfile.gettempdir(),
    os.path.join("/nfs/tmp2/", getpass.getuser()),
    os.path.join("/p/lscratch*/", getpass.getuser()),
]

"""This is the longest a failed multiproc test will take.
Barriers will time out and raise an exception after this interval.
In MPI mode, barriers don't time out (they hang).  See mpi_multiproc_test.
"""
barrier_timeout = 5

"""This is the lock timeout for expected failures.
This may need to be higher for some filesystems."""
lock_fail_timeout = 0.1


def make_readable(*paths):
    # TODO: From os.chmod doc:
    # "Note Although Windows supports chmod(), you can only
    # set the file's read-only flag with it (via the stat.S_IWRITE and
    # stat.S_IREAD constants or a corresponding integer value). All other
    # bits are ignored."
    for path in paths:
        if sys.platform != "win32":
            mode = 0o555 if os.path.isdir(path) else 0o444
        else:
            mode = stat.S_IREAD
        os.chmod(path, mode)


def make_writable(*paths):
    for path in paths:
        if sys.platform != "win32":
            mode = 0o755 if os.path.isdir(path) else 0o744
        else:
            mode = stat.S_IWRITE
        os.chmod(path, mode)


@contextmanager
def read_only(*paths):
    modes = [os.stat(p).st_mode for p in paths]
    make_readable(*paths)

    yield

    for path, mode in zip(paths, modes):
        os.chmod(path, mode)


@pytest.fixture(scope="session", params=locations)
def lock_test_directory(request):
    """This fixture causes tests to be executed for many different mounts.

    See the ``locations`` dict above for details.
    """
    return request.param


@pytest.fixture(scope="session")
def lock_dir(lock_test_directory):
    parent = next(
        (p for p in glob.glob(lock_test_directory) if os.path.exists(p) and os.access(p, os.W_OK)),
        None,
    )
    if not parent:
        # Skip filesystems that don't exist or aren't writable
        pytest.skip("requires filesystem: '%s'" % lock_test_directory)
    elif mpi and parent == tempfile.gettempdir():
        # Skip local tmp test for MPI runs
        pytest.skip("skipping local tmp directory for MPI test.")

    tempdir = None
    if not mpi or comm.rank == 0:
        tempdir = tempfile.mkdtemp(dir=parent)
    if mpi:
        tempdir = comm.bcast(tempdir)

    yield tempdir

    if mpi:
        # rank 0 may get here before others, in which case it'll try to
        # remove the directory while other processes try to re-create the
        # lock.  This will give errno 39: directory not empty.  Use a
        # barrier to ensure everyone is done first.
        comm.barrier()

    if not mpi or comm.rank == 0:
        make_writable(tempdir)
        shutil.rmtree(tempdir)


@pytest.fixture
def private_lock_path(lock_dir):
    """In MPI mode, this is a private lock for each rank in a multiproc test.

    For other modes, it is the same as a shared lock.
    """
    lock_file = os.path.join(lock_dir, "lockfile")
    if mpi:
        lock_file += ".%s" % comm.rank

    yield lock_file

    if os.path.exists(lock_file):
        make_writable(lock_dir, lock_file)
        os.unlink(lock_file)


@pytest.fixture
def lock_path(lock_dir):
    """This lock is shared among all processes in a multiproc test."""
    lock_file = os.path.join(lock_dir, "lockfile")

    yield lock_file

    if os.path.exists(lock_file):
        make_writable(lock_dir, lock_file)
        os.unlink(lock_file)


def test_poll_interval_generator():
    interval_iter = iter(lk.Lock._poll_interval_generator(_wait_times=[1, 2, 3]))
    intervals = list(next(interval_iter) for i in range(100))
    assert intervals == [1] * 20 + [2] * 40 + [3] * 40


def local_multiproc_test(*functions, **kwargs):
    """Order some processes using simple barrier synchronization."""
    b = mp.Barrier(len(functions), timeout=barrier_timeout)

    args = (b,) + tuple(kwargs.get("extra_args", ()))
    procs = [Process(target=f, args=args, name=f.__name__) for f in functions]

    for p in procs:
        p.start()

    for p in procs:
        p.join()

    assert all(p.exitcode == 0 for p in procs)


def mpi_multiproc_test(*functions):
    """SPMD version of multiproc test.

    This needs to be run like so:

           srun spack test lock

    Each process executes its corresponding function.  This is different
    from ``multiproc_test`` above, which spawns the processes. This will
    skip tests if there are too few processes to run them.
    """
    procs = len(functions)
    if procs > comm.size:
        pytest.skip("requires at least %d MPI processes" % procs)

    comm.Barrier()  # barrier before each MPI test

    include = comm.rank < len(functions)
    subcomm = comm.Split(include)

    class subcomm_barrier:
        """Stand-in for multiproc barrier for MPI-parallel jobs."""

        def wait(self):
            subcomm.Barrier()

    if include:
        try:
            functions[subcomm.rank](subcomm_barrier())
        except BaseException:
            # aborting is the best we can do for MPI tests without
            # hanging, since we're using MPI barriers. This will fail
            # early and it loses the nice pytest output, but at least it
            # gets use a stacktrace on the processes that failed.
            traceback.print_exc()
            comm.Abort()
    subcomm.Free()

    comm.Barrier()  # barrier after each MPI test.


"""``multiproc_test()`` should be called by tests below.
``multiproc_test()`` will work for either MPI runs or for local runs.
"""
multiproc_test = mpi_multiproc_test if mpi else local_multiproc_test


#
# Process snippets below can be composed into tests.
#
class AcquireWrite:
    def __init__(self, lock_path, start=0, length=0):
        self.lock_path = lock_path
        self.start = start
        self.length = length

    @property
    def __name__(self):
        return self.__class__.__name__

    def __call__(self, barrier):
        lock = lk.Lock(self.lock_path, start=self.start, length=self.length)
        lock.acquire_write()  # grab exclusive lock
        barrier.wait()
        barrier.wait()  # hold the lock until timeout in other procs.


class AcquireRead:
    def __init__(self, lock_path, start=0, length=0):
        self.lock_path = lock_path
        self.start = start
        self.length = length

    @property
    def __name__(self):
        return self.__class__.__name__

    def __call__(self, barrier):
        lock = lk.Lock(self.lock_path, start=self.start, length=self.length)
        lock.acquire_read()  # grab shared lock
        barrier.wait()
        barrier.wait()  # hold the lock until timeout in other procs.


class TimeoutWrite:
    def __init__(self, lock_path, start=0, length=0):
        self.lock_path = lock_path
        self.start = start
        self.length = length

    @property
    def __name__(self):
        return self.__class__.__name__

    def __call__(self, barrier):
        lock = lk.Lock(self.lock_path, start=self.start, length=self.length)
        barrier.wait()  # wait for lock acquire in first process
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        barrier.wait()


class TimeoutRead:
    def __init__(self, lock_path, start=0, length=0):
        self.lock_path = lock_path
        self.start = start
        self.length = length

    @property
    def __name__(self):
        return self.__class__.__name__

    def __call__(self, barrier):
        lock = lk.Lock(self.lock_path, start=self.start, length=self.length)
        barrier.wait()  # wait for lock acquire in first process
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
        barrier.wait()


#
# Test that exclusive locks on other processes time out when an
# exclusive lock is held.
#
def test_write_lock_timeout_on_write(lock_path):
    multiproc_test(AcquireWrite(lock_path), TimeoutWrite(lock_path))


def test_write_lock_timeout_on_write_2(lock_path):
    multiproc_test(AcquireWrite(lock_path), TimeoutWrite(lock_path), TimeoutWrite(lock_path))


def test_write_lock_timeout_on_write_3(lock_path):
    multiproc_test(
        AcquireWrite(lock_path),
        TimeoutWrite(lock_path),
        TimeoutWrite(lock_path),
        TimeoutWrite(lock_path),
    )


def test_write_lock_timeout_on_write_ranges(lock_path):
    multiproc_test(AcquireWrite(lock_path, 0, 1), TimeoutWrite(lock_path, 0, 1))


def test_write_lock_timeout_on_write_ranges_2(lock_path):
    multiproc_test(
        AcquireWrite(lock_path, 0, 64),
        AcquireWrite(lock_path, 65, 1),
        TimeoutWrite(lock_path, 0, 1),
        TimeoutWrite(lock_path, 63, 1),
    )


def test_write_lock_timeout_on_write_ranges_3(lock_path):
    multiproc_test(
        AcquireWrite(lock_path, 0, 1),
        AcquireWrite(lock_path, 1, 1),
        TimeoutWrite(lock_path),
        TimeoutWrite(lock_path),
        TimeoutWrite(lock_path),
    )


def test_write_lock_timeout_on_write_ranges_4(lock_path):
    multiproc_test(
        AcquireWrite(lock_path, 0, 1),
        AcquireWrite(lock_path, 1, 1),
        AcquireWrite(lock_path, 2, 456),
        AcquireWrite(lock_path, 500, 64),
        TimeoutWrite(lock_path),
        TimeoutWrite(lock_path),
        TimeoutWrite(lock_path),
    )


#
# Test that shared locks on other processes time out when an
# exclusive lock is held.
#
def test_read_lock_timeout_on_write(lock_path):
    multiproc_test(AcquireWrite(lock_path), TimeoutRead(lock_path))


def test_read_lock_timeout_on_write_2(lock_path):
    multiproc_test(AcquireWrite(lock_path), TimeoutRead(lock_path), TimeoutRead(lock_path))


def test_read_lock_timeout_on_write_3(lock_path):
    multiproc_test(
        AcquireWrite(lock_path),
        TimeoutRead(lock_path),
        TimeoutRead(lock_path),
        TimeoutRead(lock_path),
    )


def test_read_lock_timeout_on_write_ranges(lock_path):
    """small write lock, read whole file."""
    multiproc_test(AcquireWrite(lock_path, 0, 1), TimeoutRead(lock_path))


def test_read_lock_timeout_on_write_ranges_2(lock_path):
    """small write lock, small read lock"""
    multiproc_test(AcquireWrite(lock_path, 0, 1), TimeoutRead(lock_path, 0, 1))


def test_read_lock_timeout_on_write_ranges_3(lock_path):
    """two write locks, overlapping read locks"""
    multiproc_test(
        AcquireWrite(lock_path, 0, 1),
        AcquireWrite(lock_path, 64, 128),
        TimeoutRead(lock_path, 0, 1),
        TimeoutRead(lock_path, 128, 256),
    )


#
# Test that exclusive locks time out when shared locks are held.
#
def test_write_lock_timeout_on_read(lock_path):
    multiproc_test(AcquireRead(lock_path), TimeoutWrite(lock_path))


def test_write_lock_timeout_on_read_2(lock_path):
    multiproc_test(AcquireRead(lock_path), TimeoutWrite(lock_path), TimeoutWrite(lock_path))


def test_write_lock_timeout_on_read_3(lock_path):
    multiproc_test(
        AcquireRead(lock_path),
        TimeoutWrite(lock_path),
        TimeoutWrite(lock_path),
        TimeoutWrite(lock_path),
    )


def test_write_lock_timeout_on_read_ranges(lock_path):
    multiproc_test(AcquireRead(lock_path, 0, 1), TimeoutWrite(lock_path))


def test_write_lock_timeout_on_read_ranges_2(lock_path):
    multiproc_test(AcquireRead(lock_path, 0, 1), TimeoutWrite(lock_path, 0, 1))


def test_write_lock_timeout_on_read_ranges_3(lock_path):
    multiproc_test(
        AcquireRead(lock_path, 0, 1),
        AcquireRead(lock_path, 10, 1),
        TimeoutWrite(lock_path, 0, 1),
        TimeoutWrite(lock_path, 10, 1),
    )


def test_write_lock_timeout_on_read_ranges_4(lock_path):
    multiproc_test(
        AcquireRead(lock_path, 0, 64),
        TimeoutWrite(lock_path, 10, 1),
        TimeoutWrite(lock_path, 32, 1),
    )


def test_write_lock_timeout_on_read_ranges_5(lock_path):
    multiproc_test(
        AcquireRead(lock_path, 64, 128),
        TimeoutWrite(lock_path, 65, 1),
        TimeoutWrite(lock_path, 127, 1),
        TimeoutWrite(lock_path, 90, 10),
    )


#
# Test that exclusive locks time while lots of shared locks are held.
#
def test_write_lock_timeout_with_multiple_readers_2_1(lock_path):
    multiproc_test(AcquireRead(lock_path), AcquireRead(lock_path), TimeoutWrite(lock_path))


def test_write_lock_timeout_with_multiple_readers_2_2(lock_path):
    multiproc_test(
        AcquireRead(lock_path),
        AcquireRead(lock_path),
        TimeoutWrite(lock_path),
        TimeoutWrite(lock_path),
    )


def test_write_lock_timeout_with_multiple_readers_3_1(lock_path):
    multiproc_test(
        AcquireRead(lock_path),
        AcquireRead(lock_path),
        AcquireRead(lock_path),
        TimeoutWrite(lock_path),
    )


def test_write_lock_timeout_with_multiple_readers_3_2(lock_path):
    multiproc_test(
        AcquireRead(lock_path),
        AcquireRead(lock_path),
        AcquireRead(lock_path),
        TimeoutWrite(lock_path),
        TimeoutWrite(lock_path),
    )


def test_write_lock_timeout_with_multiple_readers_2_1_ranges(lock_path):
    multiproc_test(
        AcquireRead(lock_path, 0, 10), AcquireRead(lock_path, 2, 10), TimeoutWrite(lock_path, 5, 5)
    )


def test_write_lock_timeout_with_multiple_readers_2_3_ranges(lock_path):
    multiproc_test(
        AcquireRead(lock_path, 0, 10),
        AcquireRead(lock_path, 5, 15),
        TimeoutWrite(lock_path, 0, 1),
        TimeoutWrite(lock_path, 11, 3),
        TimeoutWrite(lock_path, 7, 1),
    )


def test_write_lock_timeout_with_multiple_readers_3_1_ranges(lock_path):
    multiproc_test(
        AcquireRead(lock_path, 0, 5),
        AcquireRead(lock_path, 5, 5),
        AcquireRead(lock_path, 10, 5),
        TimeoutWrite(lock_path, 0, 15),
    )


def test_write_lock_timeout_with_multiple_readers_3_2_ranges(lock_path):
    multiproc_test(
        AcquireRead(lock_path, 0, 5),
        AcquireRead(lock_path, 5, 5),
        AcquireRead(lock_path, 10, 5),
        TimeoutWrite(lock_path, 3, 10),
        TimeoutWrite(lock_path, 5, 1),
    )


@pytest.mark.skipif(getuid() == 0, reason="user is root")
def test_read_lock_on_read_only_lockfile(lock_dir, lock_path):
    """read-only directory, read-only lockfile."""
    touch(lock_path)
    with read_only(lock_path, lock_dir):
        lock = lk.Lock(lock_path)

        with lk.ReadTransaction(lock):
            pass

        with pytest.raises(lk.LockROFileError):
            with lk.WriteTransaction(lock):
                pass


def test_read_lock_read_only_dir_writable_lockfile(lock_dir, lock_path):
    """read-only directory, writable lockfile."""
    touch(lock_path)
    with read_only(lock_dir):
        lock = lk.Lock(lock_path)

        with lk.ReadTransaction(lock):
            pass

        with lk.WriteTransaction(lock):
            pass


@pytest.mark.skipif(False if sys.platform == "win32" else getuid() == 0, reason="user is root")
def test_read_lock_no_lockfile(lock_dir, lock_path):
    """read-only directory, no lockfile (so can't create)."""
    with read_only(lock_dir):
        lock = lk.Lock(lock_path)

        with pytest.raises(lk.CantCreateLockError):
            with lk.ReadTransaction(lock):
                pass

        with pytest.raises(lk.CantCreateLockError):
            with lk.WriteTransaction(lock):
                pass


def test_upgrade_read_to_write(private_lock_path):
    """Test that a read lock can be upgraded to a write lock.

    Note that to upgrade a read lock to a write lock, you have the be the
    only holder of a read lock.  Client code needs to coordinate that for
    shared locks.  For this test, we use a private lock just to test that an
    upgrade is possible.
    """
    # ensure lock file exists the first time, so we open it read-only
    # to begin with.
    touch(private_lock_path)

    lock = lk.Lock(private_lock_path)
    assert lock._reads == 0
    assert lock._writes == 0

    lock.acquire_read()
    assert lock._reads == 1
    assert lock._writes == 0
    assert lock._file.mode == "r+"

    lock.acquire_write()
    assert lock._reads == 1
    assert lock._writes == 1
    assert lock._file.mode == "r+"

    lock.release_write()
    assert lock._reads == 1
    assert lock._writes == 0
    assert lock._file.mode == "r+"

    lock.release_read()
    assert lock._reads == 0
    assert lock._writes == 0
    assert lock._file is None


def test_upgrade_read_to_write_fails_with_readonly_file(private_lock_path):
    """Test that read-only file can be read-locked but not write-locked."""
    # ensure lock file exists the first time
    touch(private_lock_path)

    # open it read-only to begin with.
    with read_only(private_lock_path):
        lock = lk.Lock(private_lock_path)
        assert lock._reads == 0
        assert lock._writes == 0

        lock.acquire_read()
        assert lock._reads == 1
        assert lock._writes == 0
        assert lock._file.mode == "r"

        # upgrade to write here
        with pytest.raises(lk.LockROFileError):
            lock.acquire_write()

        # TODO: lk.FILE_TRACKER does not release private_lock_path
        lk.FILE_TRACKER.release_by_stat(os.stat(private_lock_path))


class ComplexAcquireAndRelease:
    def __init__(self, lock_path):
        self.lock_path = lock_path

    def p1(self, barrier):
        lock = lk.Lock(self.lock_path)

        lock.acquire_write()
        barrier.wait()  # ---------------------------------------- 1
        # others test timeout
        barrier.wait()  # ---------------------------------------- 2
        lock.release_write()  # release and others acquire read
        barrier.wait()  # ---------------------------------------- 3
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 4
        lock.release_read()
        barrier.wait()  # ---------------------------------------- 5

        # p2 upgrades read to write
        barrier.wait()  # ---------------------------------------- 6
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
        barrier.wait()  # ---------------------------------------- 7
        # p2 releases write and read
        barrier.wait()  # ---------------------------------------- 8

        # p3 acquires read
        barrier.wait()  # ---------------------------------------- 9
        # p3 upgrades read to write
        barrier.wait()  # ---------------------------------------- 10
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
        barrier.wait()  # ---------------------------------------- 11
        # p3 releases locks
        barrier.wait()  # ---------------------------------------- 12
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 13
        lock.release_read()

    def p2(self, barrier):
        lock = lk.Lock(self.lock_path)

        # p1 acquires write
        barrier.wait()  # ---------------------------------------- 1
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
        barrier.wait()  # ---------------------------------------- 2
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 3
        # p1 tests shared read
        barrier.wait()  # ---------------------------------------- 4
        # others release reads
        barrier.wait()  # ---------------------------------------- 5

        lock.acquire_write()  # upgrade read to write
        barrier.wait()  # ---------------------------------------- 6
        # others test timeout
        barrier.wait()  # ---------------------------------------- 7
        lock.release_write()  # release read AND write (need both)
        lock.release_read()
        barrier.wait()  # ---------------------------------------- 8

        # p3 acquires read
        barrier.wait()  # ---------------------------------------- 9
        # p3 upgrades read to write
        barrier.wait()  # ---------------------------------------- 10
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
        barrier.wait()  # ---------------------------------------- 11
        # p3 releases locks
        barrier.wait()  # ---------------------------------------- 12
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 13
        lock.release_read()

    def p3(self, barrier):
        lock = lk.Lock(self.lock_path)

        # p1 acquires write
        barrier.wait()  # ---------------------------------------- 1
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
        barrier.wait()  # ---------------------------------------- 2
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 3
        # p1 tests shared read
        barrier.wait()  # ---------------------------------------- 4
        lock.release_read()
        barrier.wait()  # ---------------------------------------- 5

        # p2 upgrades read to write
        barrier.wait()  # ---------------------------------------- 6
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_write(lock_fail_timeout)
        with pytest.raises(lk.LockTimeoutError):
            lock.acquire_read(lock_fail_timeout)
        barrier.wait()  # ---------------------------------------- 7
        # p2 releases write & read
        barrier.wait()  # ---------------------------------------- 8

        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 9
        lock.acquire_write()
        barrier.wait()  # ---------------------------------------- 10
        # others test timeout
        barrier.wait()  # ---------------------------------------- 11
        lock.release_read()  # release read AND write in opposite
        lock.release_write()  # order from before on p2
        barrier.wait()  # ---------------------------------------- 12
        lock.acquire_read()
        barrier.wait()  # ---------------------------------------- 13
        lock.release_read()


#
# Longer test case that ensures locks are reusable. Ordering is
# enforced by barriers throughout -- steps are shown with numbers.
#
def test_complex_acquire_and_release_chain(lock_path):
    test_chain = ComplexAcquireAndRelease(lock_path)
    multiproc_test(test_chain.p1, test_chain.p2, test_chain.p3)


class AssertLock(lk.Lock):
    """Test lock class that marks acquire/release events."""

    def __init__(self, lock_path, vals):
        super().__init__(lock_path)
        self.vals = vals

    # assert hooks for subclasses
    assert_acquire_read = lambda self: None
    assert_acquire_write = lambda self: None
    assert_release_read = lambda self: None
    assert_release_write = lambda self: None

    def acquire_read(self, timeout=None):
        self.assert_acquire_read()
        result = super().acquire_read(timeout)
        self.vals["acquired_read"] = True
        return result

    def acquire_write(self, timeout=None):
        self.assert_acquire_write()
        result = super().acquire_write(timeout)
        self.vals["acquired_write"] = True
        return result

    def release_read(self, release_fn=None):
        self.assert_release_read()
        result = super().release_read(release_fn)
        self.vals["released_read"] = True
        return result

    def release_write(self, release_fn=None):
        self.assert_release_write()
        result = super().release_write(release_fn)
        self.vals["released_write"] = True
        return result


@pytest.mark.parametrize(
    "transaction,type", [(lk.ReadTransaction, "read"), (lk.WriteTransaction, "write")]
)
def test_transaction(lock_path, transaction, type):
    class MockLock(AssertLock):
        def assert_acquire_read(self):
            assert not vals["entered_fn"]
            assert not vals["exited_fn"]

        def assert_release_read(self):
            assert vals["entered_fn"]
            assert not vals["exited_fn"]

        def assert_acquire_write(self):
            assert not vals["entered_fn"]
            assert not vals["exited_fn"]

        def assert_release_write(self):
            assert vals["entered_fn"]
            assert not vals["exited_fn"]

    def enter_fn():
        # assert enter_fn is called while lock is held
        assert vals["acquired_%s" % type]
        vals["entered_fn"] = True

    def exit_fn(t, v, tb):
        # assert exit_fn is called while lock is held
        assert not vals["released_%s" % type]
        vals["exited_fn"] = True
        vals["exception"] = t or v or tb

    vals = collections.defaultdict(lambda: False)
    lock = MockLock(lock_path, vals)

    with transaction(lock, acquire=enter_fn, release=exit_fn):
        assert vals["acquired_%s" % type]
        assert not vals["released_%s" % type]

    assert vals["entered_fn"]
    assert vals["exited_fn"]
    assert vals["acquired_%s" % type]
    assert vals["released_%s" % type]
    assert not vals["exception"]


@pytest.mark.parametrize(
    "transaction,type", [(lk.ReadTransaction, "read"), (lk.WriteTransaction, "write")]
)
def test_transaction_with_exception(lock_path, transaction, type):
    class MockLock(AssertLock):
        def assert_acquire_read(self):
            assert not vals["entered_fn"]
            assert not vals["exited_fn"]

        def assert_release_read(self):
            assert vals["entered_fn"]
            assert not vals["exited_fn"]

        def assert_acquire_write(self):
            assert not vals["entered_fn"]
            assert not vals["exited_fn"]

        def assert_release_write(self):
            assert vals["entered_fn"]
            assert not vals["exited_fn"]

    def enter_fn():
        assert vals["acquired_%s" % type]
        vals["entered_fn"] = True

    def exit_fn(t, v, tb):
        assert not vals["released_%s" % type]
        vals["exited_fn"] = True
        vals["exception"] = t or v or tb
        return exit_result

    exit_result = False
    vals = collections.defaultdict(lambda: False)
    lock = MockLock(lock_path, vals)

    with pytest.raises(Exception):
        with transaction(lock, acquire=enter_fn, release=exit_fn):
            raise Exception()

    assert vals["entered_fn"]
    assert vals["exited_fn"]
    assert vals["exception"]

    # test suppression of exceptions from exit_fn
    exit_result = True
    vals.clear()

    # should not raise now.
    with transaction(lock, acquire=enter_fn, release=exit_fn):
        raise Exception()

    assert vals["entered_fn"]
    assert vals["exited_fn"]
    assert vals["exception"]


@pytest.mark.parametrize(
    "transaction,type", [(lk.ReadTransaction, "read"), (lk.WriteTransaction, "write")]
)
def test_transaction_with_context_manager(lock_path, transaction, type):
    class MockLock(AssertLock):
        def assert_acquire_read(self):
            assert not vals["entered_ctx"]
            assert not vals["exited_ctx"]

        def assert_release_read(self):
            assert vals["entered_ctx"]
            assert vals["exited_ctx"]

        def assert_acquire_write(self):
            assert not vals["entered_ctx"]
            assert not vals["exited_ctx"]

        def assert_release_write(self):
            assert vals["entered_ctx"]
            assert vals["exited_ctx"]

    class TestContextManager:
        def __enter__(self):
            vals["entered_ctx"] = True

        def __exit__(self, t, v, tb):
            assert not vals["released_%s" % type]
            vals["exited_ctx"] = True
            vals["exception_ctx"] = t or v or tb
            return exit_ctx_result

    def exit_fn(t, v, tb):
        assert not vals["released_%s" % type]
        vals["exited_fn"] = True
        vals["exception_fn"] = t or v or tb
        return exit_fn_result

    exit_fn_result, exit_ctx_result = False, False
    vals = collections.defaultdict(lambda: False)
    lock = MockLock(lock_path, vals)

    with transaction(lock, acquire=TestContextManager, release=exit_fn):
        pass

    assert vals["entered_ctx"]
    assert vals["exited_ctx"]
    assert vals["exited_fn"]
    assert not vals["exception_ctx"]
    assert not vals["exception_fn"]

    vals.clear()
    with transaction(lock, acquire=TestContextManager):
        pass

    assert vals["entered_ctx"]
    assert vals["exited_ctx"]
    assert not vals["exited_fn"]
    assert not vals["exception_ctx"]
    assert not vals["exception_fn"]

    # below are tests for exceptions with and without suppression
    def assert_ctx_and_fn_exception(raises=True):
        vals.clear()

        if raises:
            with pytest.raises(Exception):
                with transaction(lock, acquire=TestContextManager, release=exit_fn):
                    raise Exception()
        else:
            with transaction(lock, acquire=TestContextManager, release=exit_fn):
                raise Exception()

        assert vals["entered_ctx"]
        assert vals["exited_ctx"]
        assert vals["exited_fn"]
        assert vals["exception_ctx"]
        assert vals["exception_fn"]

    def assert_only_ctx_exception(raises=True):
        vals.clear()

        if raises:
            with pytest.raises(Exception):
                with transaction(lock, acquire=TestContextManager):
                    raise Exception()
        else:
            with transaction(lock, acquire=TestContextManager):
                raise Exception()

        assert vals["entered_ctx"]
        assert vals["exited_ctx"]
        assert not vals["exited_fn"]
        assert vals["exception_ctx"]
        assert not vals["exception_fn"]

    # no suppression
    assert_ctx_and_fn_exception(raises=True)
    assert_only_ctx_exception(raises=True)

    # suppress exception only in function
    exit_fn_result, exit_ctx_result = True, False
    assert_ctx_and_fn_exception(raises=False)
    assert_only_ctx_exception(raises=True)

    # suppress exception only in context
    exit_fn_result, exit_ctx_result = False, True
    assert_ctx_and_fn_exception(raises=False)
    assert_only_ctx_exception(raises=False)

    # suppress exception in function and context
    exit_fn_result, exit_ctx_result = True, True
    assert_ctx_and_fn_exception(raises=False)
    assert_only_ctx_exception(raises=False)


def test_nested_write_transaction(lock_path):
    """Ensure that the outermost write transaction writes."""

    def write(t, v, tb):
        vals["wrote"] = True

    vals = collections.defaultdict(lambda: False)
    lock = AssertLock(lock_path, vals)

    # write/write
    with lk.WriteTransaction(lock, release=write):
        assert not vals["wrote"]
        with lk.WriteTransaction(lock, release=write):
            assert not vals["wrote"]
        assert not vals["wrote"]
    assert vals["wrote"]

    # read/write
    vals.clear()
    with lk.ReadTransaction(lock):
        assert not vals["wrote"]
        with lk.WriteTransaction(lock, release=write):
            assert not vals["wrote"]
        assert vals["wrote"]

    # write/read/write
    vals.clear()
    with lk.WriteTransaction(lock, release=write):
        assert not vals["wrote"]
        with lk.ReadTransaction(lock):
            assert not vals["wrote"]
            with lk.WriteTransaction(lock, release=write):
                assert not vals["wrote"]
            assert not vals["wrote"]
        assert not vals["wrote"]
    assert vals["wrote"]

    # read/write/read/write
    vals.clear()
    with lk.ReadTransaction(lock):
        with lk.WriteTransaction(lock, release=write):
            assert not vals["wrote"]
            with lk.ReadTransaction(lock):
                assert not vals["wrote"]
                with lk.WriteTransaction(lock, release=write):
                    assert not vals["wrote"]
                assert not vals["wrote"]
            assert not vals["wrote"]
        assert vals["wrote"]


def test_nested_reads(lock_path):
    """Ensure that write transactions won't re-read data."""

    def read():
        vals["read"] += 1

    vals = collections.defaultdict(lambda: 0)
    lock = AssertLock(lock_path, vals)

    # read/read
    vals.clear()
    assert vals["read"] == 0
    with lk.ReadTransaction(lock, acquire=read):
        assert vals["read"] == 1
        with lk.ReadTransaction(lock, acquire=read):
            assert vals["read"] == 1

    # write/write
    vals.clear()
    assert vals["read"] == 0
    with lk.WriteTransaction(lock, acquire=read):
        assert vals["read"] == 1
        with lk.WriteTransaction(lock, acquire=read):
            assert vals["read"] == 1

    # read/write
    vals.clear()
    assert vals["read"] == 0
    with lk.ReadTransaction(lock, acquire=read):
        assert vals["read"] == 1
        with lk.WriteTransaction(lock, acquire=read):
            assert vals["read"] == 1

    # write/read/write
    vals.clear()
    assert vals["read"] == 0
    with lk.WriteTransaction(lock, acquire=read):
        assert vals["read"] == 1
        with lk.ReadTransaction(lock, acquire=read):
            assert vals["read"] == 1
            with lk.WriteTransaction(lock, acquire=read):
                assert vals["read"] == 1

    # read/write/read/write
    vals.clear()
    assert vals["read"] == 0
    with lk.ReadTransaction(lock, acquire=read):
        assert vals["read"] == 1
        with lk.WriteTransaction(lock, acquire=read):
            assert vals["read"] == 1
            with lk.ReadTransaction(lock, acquire=read):
                assert vals["read"] == 1
                with lk.WriteTransaction(lock, acquire=read):
                    assert vals["read"] == 1


class LockDebugOutput:
    def __init__(self, lock_path):
        self.lock_path = lock_path
        self.host = socket.gethostname()

    def p1(self, barrier, q1, q2):
        # exchange pids
        p1_pid = os.getpid()
        q1.put(p1_pid)
        p2_pid = q2.get()

        # set up lock
        lock = lk.Lock(self.lock_path, debug=True)

        with lk.WriteTransaction(lock):
            # p1 takes write lock and writes pid/host to file
            barrier.wait()  # ------------------------------------ 1

        assert lock.pid == p1_pid
        assert lock.host == self.host

        # wait for p2 to verify contents of file
        barrier.wait()  # ---------------------------------------- 2

        # wait for p2 to take a write lock
        barrier.wait()  # ---------------------------------------- 3

        # verify pid/host info again
        with lk.ReadTransaction(lock):
            assert lock.old_pid == p1_pid
            assert lock.old_host == self.host

            assert lock.pid == p2_pid
            assert lock.host == self.host

        barrier.wait()  # ---------------------------------------- 4

    def p2(self, barrier, q1, q2):
        # exchange pids
        p2_pid = os.getpid()
        p1_pid = q1.get()
        q2.put(p2_pid)

        # set up lock
        lock = lk.Lock(self.lock_path, debug=True)

        # p1 takes write lock and writes pid/host to file
        barrier.wait()  # ---------------------------------------- 1

        # verify that p1 wrote information to lock file
        with lk.ReadTransaction(lock):
            assert lock.pid == p1_pid
            assert lock.host == self.host

        barrier.wait()  # ---------------------------------------- 2

        # take a write lock on the file and verify pid/host info
        with lk.WriteTransaction(lock):
            assert lock.old_pid == p1_pid
            assert lock.old_host == self.host

            assert lock.pid == p2_pid
            assert lock.host == self.host

            barrier.wait()  # ------------------------------------ 3

        # wait for p1 to verify pid/host info
        barrier.wait()  # ---------------------------------------- 4


def test_lock_debug_output(lock_path):
    test_debug = LockDebugOutput(lock_path)
    q1, q2 = Queue(), Queue()
    local_multiproc_test(test_debug.p2, test_debug.p1, extra_args=(q1, q2))


def test_lock_with_no_parent_directory(tmpdir):
    """Make sure locks work even when their parent directory does not exist."""
    with tmpdir.as_cwd():
        lock = lk.Lock("foo/bar/baz/lockfile")
        with lk.WriteTransaction(lock):
            pass


def test_lock_in_current_directory(tmpdir):
    """Make sure locks work even when their parent directory does not exist."""
    with tmpdir.as_cwd():
        # test we can create a lock in the current directory
        lock = lk.Lock("lockfile")
        for i in range(10):
            with lk.ReadTransaction(lock):
                pass
            with lk.WriteTransaction(lock):
                pass

        # and that we can do the same thing after it's already there
        lock = lk.Lock("lockfile")
        for i in range(10):
            with lk.ReadTransaction(lock):
                pass
            with lk.WriteTransaction(lock):
                pass


def test_attempts_str():
    assert lk._attempts_str(0, 0) == ""
    assert lk._attempts_str(0.12, 1) == ""
    assert lk._attempts_str(12.345, 2) == " after 12.345s and 2 attempts"


def test_lock_str():
    lock = lk.Lock("lockfile")
    lockstr = str(lock)
    assert "lockfile[0:0]" in lockstr
    assert "timeout=None" in lockstr
    assert "#reads=0, #writes=0" in lockstr


def test_downgrade_write_okay(tmpdir):
    """Test the lock write-to-read downgrade operation."""
    with tmpdir.as_cwd():
        lock = lk.Lock("lockfile")
        lock.acquire_write()
        lock.downgrade_write_to_read()
        assert lock._reads == 1
        assert lock._writes == 0
        lock.release_read()


def test_downgrade_write_fails(tmpdir):
    """Test failing the lock write-to-read downgrade operation."""
    with tmpdir.as_cwd():
        lock = lk.Lock("lockfile")
        lock.acquire_read()
        msg = "Cannot downgrade lock from write to read on file: lockfile"
        with pytest.raises(lk.LockDowngradeError, match=msg):
            lock.downgrade_write_to_read()
        lock.release_read()


@pytest.mark.parametrize(
    "err_num,err_msg",
    [
        (errno.EACCES, "Fake EACCES error"),
        (errno.EAGAIN, "Fake EAGAIN error"),
        (errno.ENOENT, "Fake ENOENT error"),
    ],
)
def test_poll_lock_exception(tmpdir, monkeypatch, err_num, err_msg):
    """Test poll lock exception handling."""

    def _lockf(fd, cmd, len, start, whence):
        raise IOError(err_num, err_msg)

    with tmpdir.as_cwd():
        lockfile = "lockfile"
        lock = lk.Lock(lockfile)
        lock.acquire_read()

        monkeypatch.setattr(fcntl, "lockf", _lockf)

        if err_num in [errno.EAGAIN, errno.EACCES]:
            assert not lock._poll_lock(fcntl.LOCK_EX)
        else:
            with pytest.raises(IOError, match=err_msg):
                lock._poll_lock(fcntl.LOCK_EX)

        monkeypatch.undo()
        lock.release_read()


def test_upgrade_read_okay(tmpdir):
    """Test the lock read-to-write upgrade operation."""
    with tmpdir.as_cwd():
        lock = lk.Lock("lockfile")
        lock.acquire_read()
        lock.upgrade_read_to_write()
        assert lock._reads == 0
        assert lock._writes == 1
        lock.release_write()


def test_upgrade_read_fails(tmpdir):
    """Test failing the lock read-to-write upgrade operation."""
    with tmpdir.as_cwd():
        lock = lk.Lock("lockfile")
        lock.acquire_write()
        msg = "Cannot upgrade lock from read to write on file: lockfile"
        with pytest.raises(lk.LockUpgradeError, match=msg):
            lock.upgrade_read_to_write()
        lock.release_write()
