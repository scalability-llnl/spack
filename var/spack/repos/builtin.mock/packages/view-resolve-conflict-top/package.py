# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ViewResolveConflictTop(Package):
    """Package for testing edge cases for views, such as spec ordering and clashing files referring
    to the same file on disk. See test_env_view_resolves_identical_file_conflicts."""

    has_code = False

    version("0.1.0")
    depends_on("view-file")
    depends_on("view-resolve-conflict-middle")

    def install(self, spec, prefix):
        middle = spec["view-resolve-conflict-middle"].prefix
        bottom = spec["view-file"].prefix
        os.mkdir(os.path.join(prefix, "bin"))
        os.symlink(os.path.join(bottom, "bin", "x"), os.path.join(prefix, "bin", "x"))
        os.symlink(os.path.join(middle, "bin", "y"), os.path.join(prefix, "bin", "y"))
