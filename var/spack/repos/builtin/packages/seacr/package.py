# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Seacr(Package):
    """SEACR (Sparse Enrichment Analysis for CUT&RUN) is intended to call peaks and
    enriched regions from sparse CUT&RUN or chromatin profiling data in which the
    background is dominated by zeros"""

    homepage = "https://github.com/FredHutch/SEACR"
    git = "https://github.com/FredHutch/SEACR.git"

    license("GPL-2.0-only", checked_by="A-N-Other")

    version("1.4-b2", tag="v1.4-beta.2", commit="5179a70494eb129fcb1d640177de73f6509654e7")
    version("1.3", tag="v1.3", commit="5a0efe59f06fb17cf9d34d415bb0c1a1f7a77a3c", preferred=True)

    # Dependencies as per the README.md
    depends_on("r", type="run")
    depends_on("bedtools2", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        script_name = f"SEACR_{self.version.up_to(2)}"
        os.chmod(f"{script_name}.sh", 0o755)
        install(f"{script_name}.sh", prefix.bin.SEACR)
        install(f"{script_name}.R", prefix.bin)
