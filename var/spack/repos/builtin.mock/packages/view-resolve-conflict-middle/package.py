# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ViewResolveConflictMiddle(Package):
    """See view-resolve-conflict-top"""

    has_code = False

    version("0.1.0")
    depends_on("view-file")

    def install(self, spec, prefix):
        bottom = spec["view-file"].prefix
        os.mkdir(os.path.join(prefix, "bin"))
        os.symlink(os.path.join(bottom, "bin", "x"), os.path.join(prefix, "bin", "x"))
        os.symlink(os.path.join(bottom, "bin", "x"), os.path.join(prefix, "bin", "y"))
