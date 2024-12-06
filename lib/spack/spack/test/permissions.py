# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import stat

import pytest

import llnl.util.filesystem as fs

from spack.util.file_permissions import InvalidPermissionsError, set_permissions

pytestmark = pytest.mark.not_on_windows("chmod unsupported on Windows")


def ensure_known_group(path):
    """Ensure that the group of a file is one that's actually in our group list.

    On systems with remote groups, the primary user group may be remote and may not
    exist on the local system (i.e., it might just be a number). Trying to use chmod to
    setgid can fail silently in situations like this.
    """
    uid = os.getuid()
    gid = fs.group_ids(uid)[0]
    os.chown(path, uid, gid)


def test_chmod_real_entries_ignores_suid_sgid(tmpdir):
    path = str(tmpdir.join("file").ensure())
    mode = stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX
    os.chmod(path, mode)
    mode = os.stat(path).st_mode  # adds a high bit we aren't concerned with

    perms = stat.S_IRWXU
    set_permissions(path, perms)

    assert os.stat(path).st_mode == mode | perms & ~stat.S_IXUSR


def test_chmod_rejects_group_writable_suid(tmpdir):
    path = str(tmpdir.join("file").ensure())
    mode = stat.S_ISUID
    fs.chmod_x(path, mode)

    perms = stat.S_IWGRP
    with pytest.raises(InvalidPermissionsError):
        set_permissions(path, perms)


def test_chmod_rejects_world_writable_suid(tmpdir):
    path = str(tmpdir.join("file").ensure())
    mode = stat.S_ISUID
    fs.chmod_x(path, mode)

    perms = stat.S_IWOTH
    with pytest.raises(InvalidPermissionsError):
        set_permissions(path, perms)


def test_chmod_rejects_world_writable_sgid(tmpdir):
    path = str(tmpdir.join("file").ensure())
    ensure_known_group(path)

    mode = stat.S_ISGID
    fs.chmod_x(path, mode)

    perms = stat.S_IWOTH
    with pytest.raises(InvalidPermissionsError):
        set_permissions(path, perms)
