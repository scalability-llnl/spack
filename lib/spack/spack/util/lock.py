# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Wrapper for ``llnl.util.lock`` allows locking to be enabled/disabled."""
import os
import stat
import sys
from typing import Optional, Tuple

import llnl.util.lock

# import some llnl.util.lock names as though they're part of spack.util.lock
from llnl.util.lock import LockError  # noqa: F401
from llnl.util.lock import LockTimeoutError  # noqa: F401
from llnl.util.lock import LockUpgradeError  # noqa: F401
from llnl.util.lock import ReadTransaction  # noqa: F401
from llnl.util.lock import WriteTransaction  # noqa: F401

import spack.error


class Lock(llnl.util.lock.Lock):
    """Lock that can be disabled.

    This overrides the ``_lock()`` and ``_unlock()`` methods from
    ``llnl.util.lock`` so that all the lock API calls will succeed, but
    the actual locking mechanism can be disabled via ``_enable_locks``.
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
        enable: Optional[bool] = None,
    ) -> None:
        enable_lock = enable
        if sys.platform == "win32":
            enable_lock = False
        elif sys.platform != "win32" and enable_lock is None:
            enable_lock = True
        self._enable = enable_lock
        super().__init__(
            path,
            start=start,
            length=length,
            default_timeout=default_timeout,
            debug=debug,
            desc=desc,
        )

    def _lock(self, op: int, timeout: Optional[float] = 0.0) -> Tuple[float, int]:
        if self._enable:
            return super()._lock(op, timeout)
        return 0.0, 0

    def _unlock(self) -> None:
        """Unlock call that always succeeds."""
        if self._enable:
            super()._unlock()

    def cleanup(self, *args) -> None:
        if self._enable:
            super().cleanup(*args)


def check_lock_safety(path: str) -> None:
    """Do some extra checks to ensure disabling locks is safe.

    This will raise an error if ``path`` can is group- or world-writable
    AND the current user can write to the directory (i.e., if this user
    AND others could write to the path).

    This is intended to run on the Spack prefix, but can be run on any
    path for testing.
    """
    if os.access(path, os.W_OK):
        stat_result = os.stat(path)
        uid, gid = stat_result.st_uid, stat_result.st_gid
        mode = stat_result[stat.ST_MODE]

        writable = None
        if (mode & stat.S_IWGRP) and (uid != gid):
            # spack is group-writeable and the group is not the owner
            writable = "group"
        elif mode & stat.S_IWOTH:
            # spack is world-writeable
            writable = "world"

        if writable:
            msg = f"Refusing to disable locks: spack is {writable}-writable."
            long_msg = (
                f"Running a shared spack without locks is unsafe. You must "
                f"restrict permissions on {path} or enable locks."
            )
            raise spack.error.SpackError(msg, long_msg)
