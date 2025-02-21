# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ViewDir(Package):
    """Installs a <prefix>/bin/x where x is a dir, in contrast to view-file."""

    has_code = False

    version("0.1.0")

    def install(self, spec, prefix):
        os.mkdir(os.path.join(prefix, "bin"))
        os.mkdir(os.path.join(prefix, "bin", "x"))
        with open(os.path.join(prefix, "bin", "x", "file_in_dir"), "wb") as f:
            f.write(b"hello world")
