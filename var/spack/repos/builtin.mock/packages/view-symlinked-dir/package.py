# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ViewSymlinkedDir(Package):
    """Installs <prefix>/bin/x/file_in_symlinked_dir where x -> y is a symlinked dir.
    This should be mergeable with view-dir, but not with view-file."""

    has_code = False

    version("0.1.0")

    def install(self, spec, prefix):
        os.mkdir(os.path.join(prefix, "bin"))
        os.mkdir(os.path.join(prefix, "bin", "y"))
        with open(os.path.join(prefix, "bin", "y", "file_in_symlinked_dir"), "wb") as f:
            f.write(b"hello world")
        os.symlink("y", os.path.join(prefix, "bin", "x"))
