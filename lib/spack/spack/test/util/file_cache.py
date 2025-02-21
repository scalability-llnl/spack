# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test Spack's FileCache."""
import os

import pytest

import llnl.util.filesystem as fs

from spack.util.file_cache import CacheError, FileCache


@pytest.fixture()
def file_cache(tmpdir):
    """Returns a properly initialized FileCache instance"""
    return FileCache(str(tmpdir))


def test_write_and_read_cache_file(file_cache):
    """Test writing then reading a cached file."""
    with file_cache.write_transaction("test.yaml") as (old, new):
        assert old is None
        assert new is not None
        new.write("foobar\n")

    with file_cache.read_transaction("test.yaml") as stream:
        text = stream.read()
        assert text == "foobar\n"


def test_read_before_init(file_cache):
    with file_cache.read_transaction("test.yaml") as stream:
        assert stream is None


@pytest.mark.not_on_windows("Locks not supported on Windows")
def test_failed_write_and_read_cache_file(file_cache):
    """Test failing to write then attempting to read a cached file."""
    with pytest.raises(RuntimeError, match=r"^foobar$"):
        with file_cache.write_transaction("test.yaml") as (old, new):
            assert old is None
            assert new is not None
            raise RuntimeError("foobar")

    # Cache dir should have exactly one (lock) file
    assert os.listdir(file_cache.root) == [".test.yaml.lock"]

    # File does not exist
    assert not file_cache.init_entry("test.yaml")


def test_write_and_remove_cache_file(file_cache):
    """Test two write transactions on a cached file. Then try to remove an
    entry from it.
    """

    with file_cache.write_transaction("test.yaml") as (old, new):
        assert old is None
        assert new is not None
        new.write("foobar\n")

    with file_cache.write_transaction("test.yaml") as (old, new):
        assert old is not None
        text = old.read()
        assert text == "foobar\n"
        assert new is not None
        new.write("barbaz\n")

    with file_cache.read_transaction("test.yaml") as stream:
        text = stream.read()
        assert text == "barbaz\n"

    file_cache.remove("test.yaml")

    # After removal the file should not exist
    assert not os.path.exists(file_cache.cache_path("test.yaml"))

    # Whether the lock file exists is more of an implementation detail, on Linux they
    # continue to exist, on Windows they don't.
    # assert os.path.exists(file_cache._lock_path('test.yaml'))


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
def test_cache_init_entry_fails(file_cache):
    """Test init_entry failures."""
    relpath = fs.join_path("test-dir", "read-only-file.txt")
    cachefile = file_cache.cache_path(relpath)
    fs.touchp(cachefile)

    # Ensure directory causes exception
    with pytest.raises(CacheError, match="not a file"):
        file_cache.init_entry(os.path.dirname(relpath))

    # Ensure non-readable file causes exception
    os.chmod(cachefile, 0o200)
    with pytest.raises(CacheError, match="Cannot access cache file"):
        file_cache.init_entry(relpath)

    # Ensure read-only parent causes exception
    relpath = fs.join_path("test-dir", "another-file.txxt")
    cachefile = file_cache.cache_path(relpath)
    os.chmod(os.path.dirname(cachefile), 0o400)
    with pytest.raises(CacheError, match="Cannot access cache dir"):
        file_cache.init_entry(relpath)


def test_cache_write_readonly_cache_fails(file_cache):
    """Test writing a read-only cached file."""
    filename = "read-only-file.txt"
    path = file_cache.cache_path(filename)
    fs.touch(path)
    os.chmod(path, 0o400)

    with pytest.raises(CacheError, match="Insufficient permissions to write"):
        file_cache.write_transaction(filename)


@pytest.mark.regression("31475")
def test_delete_is_idempotent(file_cache):
    """Deleting a non-existent key should be idempotent, to simplify life when
    running delete with multiple processes"""
    file_cache.remove("test.yaml")
