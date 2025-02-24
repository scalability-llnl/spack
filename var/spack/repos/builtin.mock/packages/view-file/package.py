# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ViewFile(Package):
    """Installs a <prefix>/bin/x where x is a file, in contrast to view-dir"""

    has_code = False

    version("0.1.0")

    def install(self, spec, prefix):
        os.mkdir(os.path.join(prefix, "bin"))
        with open(os.path.join(prefix, "bin", "x"), "wb") as f:
            f.write(b"file")
