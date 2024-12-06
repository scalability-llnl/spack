# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GitFatGit(Package):
    """Simple way to handle fat files without committing them to git, supports
    synchronization using rsync"""

    homepage = "https://github.com/jedbrown/git-fat"
    git = "https://github.com/jedbrown/git-fat.git"

    license("BSD-2-Clause")

    version("2018-08-21", commit="e1733b1c7c4169d0a1d31cb76f168fb0880176c0")

    depends_on("python", type="run")
    depends_on("git", type="run")
    depends_on("rsync", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)
