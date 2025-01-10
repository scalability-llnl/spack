# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFilelock(RPackage):
    """Portable File Locking.

    Place an exclusive or shared lock on a file. It uses 'LockFile' on Windows
    and 'fcntl' locks on Unix-like systems."""

    cran = "filelock"

    license("MIT")

    version("1.0.3", sha256="2dcd0ec453f5ec4d96f69b0c472569d57d3c5f9956a82a48492ee02f12071137")
    version("1.0.2", sha256="ac2915950789b16c43a625a2b8dab6ba423588db4a7d0daa75b74518b82b1403")

    depends_on("r@3.4:", type=("build", "run"), when="@1.0.3:")
