# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDirExpiry(RPackage):
    """Managing Expiration for Cache Directories.

    Implements an expiration system for access to versioned directories.
    Directories that have not been accessed by a registered function within a
    certain time frame are deleted. This aims to reduce disk usage by
    eliminating obsolete caches generated by old versions of packages."""

    bioc = "dir.expiry"

    version("1.14.0", commit="350a482fb2acc124f5115babfbd06b7d32fd1f6f")
    version("1.12.0", commit="141ea0d286e6851ac844216734f7ceb40c8c5fe7")
    version("1.10.0", commit="58c7811e19baa99d9f58dc65845fa6cb26f52009")
    version("1.8.0", commit="271f76cb2e8565817400e85fcc2c595923af4af6")

    depends_on("r-filelock", type=("build", "run"))
