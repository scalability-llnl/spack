# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for Spack's wrapper module around llnl.util.lock."""
import os

import pytest

from llnl.util.filesystem import getuid, group_ids

import spack.error
import spack.util.lock as lk


def test_disable_locking(tmpdir):
    """Ensure that locks do no real locking when disabled."""
    lock_path = str(tmpdir.join("lockfile"))
    lock = lk.Lock(lock_path, enable=False)

    lock.acquire_read()
    assert not os.path.exists(lock_path)

    lock.acquire_write()
    assert not os.path.exists(lock_path)

    lock.release_write()
    assert not os.path.exists(lock_path)

    lock.release_read()
    assert not os.path.exists(lock_path)


# "Disable" mock_stage fixture to avoid subdir permissions issues on cleanup.
@pytest.mark.nomockstage
def test_lock_checks_user(tmpdir):
    """Ensure lock checks work with a self-owned, self-group repo."""
    uid = getuid()
    if uid not in group_ids():
        pytest.skip("user has no group with gid == uid")

    # self-owned, own group
    tmpdir.chown(uid, uid)

    # safe
    path = str(tmpdir)
    tmpdir.chmod(0o744)
    lk.check_lock_safety(path)

    # safe
    tmpdir.chmod(0o774)
    lk.check_lock_safety(path)

    # unsafe
    tmpdir.chmod(0o777)
    with pytest.raises(spack.error.SpackError):
        lk.check_lock_safety(path)

    # safe
    tmpdir.chmod(0o474)
    lk.check_lock_safety(path)

    # safe
    tmpdir.chmod(0o477)
    lk.check_lock_safety(path)


# "Disable" mock_stage fixture to avoid subdir permissions issues on cleanup.
@pytest.mark.nomockstage
def test_lock_checks_group(tmpdir):
    """Ensure lock checks work with a self-owned, non-self-group repo."""
    uid = getuid()
    gid = next((g for g in group_ids() if g != uid), None)
    if not gid:
        pytest.skip("user has no group with gid != uid")

    # self-owned, another group
    tmpdir.chown(uid, gid)

    # safe
    path = str(tmpdir)
    tmpdir.chmod(0o744)
    lk.check_lock_safety(path)

    # unsafe
    tmpdir.chmod(0o774)
    with pytest.raises(spack.error.SpackError):
        lk.check_lock_safety(path)

    # unsafe
    tmpdir.chmod(0o777)
    with pytest.raises(spack.error.SpackError):
        lk.check_lock_safety(path)

    # safe
    tmpdir.chmod(0o474)
    lk.check_lock_safety(path)

    # safe
    tmpdir.chmod(0o477)
    lk.check_lock_safety(path)
