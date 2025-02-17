# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Mspc(Package):
    """Using combined evidence from replicates to evaluate ChIP-seq peaks"""

    homepage = "https://genometric.github.io/MSPC/"
    url = "https://github.com/Genometric/MSPC/releases/download/v6.0.1/mspc.zip"

    license("GPL-3.0-only")

    version(
        "6.0.1",
        sha256="787c813f3c30d176ed467334a514a6d980d91d6e0d6a4a6ca8420e5153e3d05a",
        expand=False,
    )

    depends_on("dotnet-core-sdk", type="run")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        # install the extracted source
        # ... ignore_errors=1 here, as otherwise it fails on the warning message from unzip
        unzip = which("unzip")
        unzip("-q", self.stage.archive_file, "-d", prefix.release, ignore_errors=1)
        # set up the helper
        install(join_path(os.path.dirname(__file__), "mspc.sh"), prefix.bin.mspc)
        set_executable(prefix.bin.mspc)
        filter_file("TARGET", join_path(prefix.release, "mspc.dll"), prefix.bin.mspc)
