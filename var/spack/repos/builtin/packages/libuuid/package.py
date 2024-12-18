# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Libuuid(AutotoolsPackage, SourceforgePackage):
    """Portable uuid C library"""

    homepage = "https://sourceforge.net/projects/libuuid/"
    sourceforge_mirror_path = "libuuid/libuuid-1.0.3.tar.gz"

    version(
        "1.0.3",
        sha256="46af3275291091009ad7f1b899de3d0cea0252737550e7919d17237997db5644",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    if sys.platform not in ["darwin", "win32"]:
        provides("uuid")

    conflicts("%gcc@14:")
